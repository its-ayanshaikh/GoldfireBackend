"""
Seed sample POS sales (bills) + customers so the admin, POS, dashboard and
return/replace flows are testable end-to-end.

It drives the REAL create_bill API (via DRF test client) so the generated
data is fully consistent with production logic — stock is decremented, the
per-purchase-lot StockIn ledger is written, BillItem.purchase_item is set,
payments + commissions are recorded. This also serves as an integration
test of the inventory changes.

Sales use the walk-in customer (phone 0000000000) on purpose: create_bill
skips its PDF/WhatsApp invoice step for that customer, which avoids the
Windows-only invoice path and external WhatsApp calls during seeding.

Usage:
    python manage.py seed_pos_sales                 # seed if no bills yet
    python manage.py seed_pos_sales --force         # seed even if bills exist
    python manage.py seed_pos_sales --branch 1 --count 12
"""
import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.db.models import Sum
from rest_framework.test import APIClient

from accounts.models import User
from employee.models import Employee
from product.models import Product, ProductVariant, Stock
from vendor.models import PurchaseItem, StockIn
from pos.models import Bill, Customer


SAMPLE_CUSTOMERS = [
    {"name": "Rahul Sharma", "phone": "9811100001"},
    {"name": "Priya Verma", "phone": "9811100002"},
    {"name": "Imran Khan", "phone": "9811100003"},
    {"name": "Sneha Patel", "phone": "9811100004"},
]


class Command(BaseCommand):
    help = "Seed sample POS customers and sales (bills) via the real create_bill API."

    def add_arguments(self, parser):
        parser.add_argument("--branch", type=int, default=1, help="Branch id to sell from (default 1)")
        parser.add_argument("--count", type=int, default=12, help="Number of sample bills (default 12)")
        parser.add_argument("--force", action="store_true", help="Seed even if bills already exist")

    def handle(self, *args, **options):
        branch_id = options["branch"]
        count = options["count"]

        # The DRF test client sends requests with host "testserver"; allow it
        # for the duration of this seeding command only.
        from django.conf import settings
        if "testserver" not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS.append("testserver")

        if Bill.objects.exists() and not options["force"]:
            self.stdout.write(self.style.WARNING(
                f"{Bill.objects.count()} bill(s) already exist. Use --force to add more sample bills. Skipping."
            ))
            # still ensure customers exist
            self._ensure_customers()
            return

        # Walk-in customer (create_bill skips PDF/WhatsApp for phone 0000000000)
        walkin, _ = Customer.objects.get_or_create(
            phone="0000000000", defaults={"name": "Walk-in Customer"}
        )
        self._ensure_customers()

        cashier = User.objects.filter(role="cashier", branch_id=branch_id).first()
        if not cashier:
            raise CommandError(
                f"No cashier user found for branch id={branch_id}. "
                f"Create a POS user for that branch first."
            )

        salespeople = list(Employee.objects.filter(branch_id=branch_id).values_list("id", flat=True)[:6])

        client = APIClient()
        client.force_authenticate(user=cashier)

        created_bill_ids = []
        failures = 0
        now = timezone.now()

        for i in range(count):
            line_items = self._pick_sellable_items(branch_id, max_lines=random.choice([1, 1, 2]))
            if not line_items:
                self.stdout.write(self.style.WARNING("No more sellable stock found; stopping early."))
                break

            items_payload = []
            expected_total = Decimal(0)
            for prod, variant, price, qty in line_items:
                items_payload.append({
                    "product_id": prod.id,
                    "variant_id": variant.id if variant else None,
                    "qty": qty,
                    "price": float(price),
                    "discount_type": "fixed",
                    "discount_value": 0,
                    "salesperson_id": random.choice(salespeople) if salespeople else None,
                })
                expected_total += price * qty

            payload = {
                "customer": {"name": walkin.name, "phone": walkin.phone},
                "items": items_payload,
                "payment": {"payment_method": "cash", "cash_amount": float(expected_total)},
                "is_gst": False,
            }

            resp = client.post("/api/pos/bills/create/", payload, format="json")
            if resp.status_code in (200, 201) and isinstance(resp.data, dict) and resp.data.get("success"):
                bill_id = resp.data.get("bill_id")
                created_bill_ids.append(bill_id)

                # Spread bills across the last ~5 months for a nicer dashboard
                # trend (bill.date is auto_now_add, so bypass it via .update()).
                month_offset = i % 5
                day_offset = random.randint(0, 25)
                back_date = now - timedelta(days=month_offset * 30 + day_offset)
                Bill.objects.filter(id=bill_id).update(date=back_date)

                self.stdout.write(self.style.SUCCESS(
                    f"Bill #{bill_id} ({resp.data.get('bill_number')}) - Rs.{resp.data.get('final_amount')}"
                ))
            else:
                failures += 1
                err = resp.data if hasattr(resp, "data") else resp.content
                self.stdout.write(self.style.ERROR(f"Bill failed ({resp.status_code}): {err}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Created {len(created_bill_ids)} sample bills"
            + (f", {failures} failed." if failures else ".")
        ))

    # ------------------------------------------------------------------
    def _ensure_customers(self):
        for c in SAMPLE_CUSTOMERS:
            Customer.objects.get_or_create(phone=c["phone"], defaults={"name": c["name"]})
        self.stdout.write(f"Sample customers ensured ({len(SAMPLE_CUSTOMERS)} named + walk-in).")

    def _pick_sellable_items(self, branch_id, max_lines=1):
        """
        Pick up to `max_lines` distinct products currently sellable in the
        branch: non-warranty, aggregate stock >= qty, and at least one
        purchase lot with positive ledger balance (so the sale can be
        attributed to a real purchase).
        """
        candidates = (
            Stock.objects.filter(
                branch_id=branch_id, qty__gt=1, product__is_warranty_item=False,
                variant__isnull=False,
            )
            .select_related("product", "variant")
            .order_by("?")[:30]
        )

        picked = []
        used_products = set()
        for s in candidates:
            if len(picked) >= max_lines:
                break
            if s.product_id in used_products:
                continue

            # confirm a purchase lot has balance in this branch
            lot = (
                PurchaseItem.objects.filter(product=s.product, variant=s.variant)
                .order_by("id")
                .first()
            )
            if not lot:
                continue
            lot_balance = StockIn.objects.filter(
                purchase_item=lot, branch_id=branch_id
            ).aggregate(t=Sum("qty"))["t"] or 0
            if lot_balance <= 0:
                continue

            price = s.variant.selling_price or lot.selling_price or Decimal("500")
            qty = 1  # keep qty=1 so cumulative sales never exceed stock
            if s.qty < qty:
                continue

            picked.append((s.product, s.variant, Decimal(price), qty))
            used_products.add(s.product_id)

        return picked
