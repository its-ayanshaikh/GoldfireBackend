# import csv
# from datetime import datetime
# from decimal import Decimal

# import os
# from django.db import transaction
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
# django.setup()

# from vendor.models import Vendor, Purchase  # app name adjust kar lena

# CSV_FILE_PATH = "data/purchase.csv"  # yaha apna path de dena


# def parse_date(date_str: str):
#     """
#     CSV me date aa rahi hai: 24/01/2026
#     """
#     if not date_str:
#         return None
#     return datetime.strptime(date_str.strip(), "%d/%m/%Y").date()


# @transaction.atomic
# def run_import():
#     created = 0
#     skipped = 0

#     with open(CSV_FILE_PATH, "r", encoding="utf-8") as f:
#         reader = csv.DictReader(f)

#         for row in reader:
#             try:
#                 vendor_id = int(row["vendor_id"])
#                 vendor = Vendor.objects.get(id=vendor_id)

#                 bill_no = (row.get("bill_no") or "").strip() or None
#                 purchase_date = parse_date(row.get("purchase_date"))

#                 total_raw = row.get("total") or "0"
#                 total = Decimal(str(total_raw).strip())

#                 notes = row.get("notes")
#                 if notes is not None:
#                     notes = notes.strip()
#                 notes = notes or None

#                 # ---- Purchase create ----
#                 Purchase.objects.create(
#                     vendor=vendor,
#                     bill_no=bill_no,
#                     purchase_date=purchase_date,
#                     total=total,
#                     notes=notes,
#                 )

#                 created += 1

#             except Vendor.DoesNotExist:
#                 print(f"❌ Vendor not found for vendor_id={row.get('vendor_id')}. Skipping row.")
#                 skipped += 1

#             except Exception as e:
#                 print(f"❌ Error in row: {row} | Error: {e}")
#                 skipped += 1

#     print(f"\n✅ Import done! Created={created}, Skipped={skipped}")


# if __name__ == "__main__":
#     run_import()


# import os
# import django
# import csv
# from decimal import Decimal

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
# django.setup()

# from vendor.models import Purchase, PurchaseItem
# from product.models import Product

# CSV_FILE_PATH = 'data/purchase_items.csv'


# def clean_key(key):
#     """ remove BOM, spaces, lowercase """
#     return key.replace('\ufeff', '').strip().lower()


# def get_fk(model, value):
#     if not value or str(value).strip() in ('0', ''):
#         return None
#     try:
#         return model.objects.get(id=int(value))
#     except model.DoesNotExist:
#         print(f"❌ FK not found: {model.__name__} id={value}")
#         return None


# def run():
#     items = []

#     with open(CSV_FILE_PATH, newline='', encoding='utf-8-sig') as file:
#         reader = csv.DictReader(file)

#         # 🔥 normalize headers
#         reader.fieldnames = [clean_key(h) for h in reader.fieldnames]

#         for raw_row in reader:
#             row = {clean_key(k): v for k, v in raw_row.items()}

#             purchase = get_fk(Purchase, row.get('purchase_id'))
#             product = get_fk(Product, row.get('product_id'))

#             if not purchase or not product:
#                 continue

#             qty = int(row.get('qty') or 0)
#             purchase_price = Decimal(row.get('purchase_price') or 0)
#             selling_price = Decimal(row.get('selling_price') or 0)

#             total = purchase_price * qty

#             item = PurchaseItem(
#                 purchase=purchase,
#                 product=product,
#                 qty=qty,
#                 purchase_price=purchase_price,
#                 selling_price=selling_price,
#                 total=total
#             )

#             items.append(item)

#     PurchaseItem.objects.bulk_create(items)
#     print(f"✅ {len(items)} purchase items imported successfully!")


# if __name__ == "__main__":
#     run()


import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
django.setup()

from vendor.models import PurchaseItem
from django.db import transaction

CSV_FILE_PATH = 'data/purchase_items.csv'


def clean_key(key):
    return key.replace('\ufeff', '').strip().lower()


def run():
    updated = 0
    skipped = 0
    not_found = 0

    with open(CSV_FILE_PATH, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [clean_key(h) for h in reader.fieldnames]

        with transaction.atomic():
            for raw_row in reader:
                row = {clean_key(k): v for k, v in raw_row.items()}

                purchaseitem_id = row.get('purchaseitem_id')
                barcode = row.get('barcode')

                if not purchaseitem_id or not barcode:
                    skipped += 1
                    continue

                try:
                    item = PurchaseItem.objects.get(id=int(purchaseitem_id))
                except PurchaseItem.DoesNotExist:
                    print(f"❌ PurchaseItem not found: id={purchaseitem_id}")
                    not_found += 1
                    continue

                # ✅ barcode fill / overwrite
                item.barcode = barcode.strip()
                item.save(update_fields=['barcode'])
                updated += 1

    print("================================")
    print(f"✅ Updated   : {updated}")
    print(f"⚠️ Skipped   : {skipped}")
    print(f"❌ Not found : {not_found}")
    print("================================")


if __name__ == "__main__":
    run()
