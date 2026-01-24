# import os
# import django
# import csv

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
# django.setup()

# from product.models import Stock, Product
# from company.models import Branch   # agar Branch yahan ho

# CSV_FILE_PATH = 'data/quantity.csv'


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
#     stocks = []

#     with open(CSV_FILE_PATH, newline='', encoding='utf-8-sig') as file:
#         reader = csv.DictReader(file)

#         # 🔥 normalize headers
#         reader.fieldnames = [clean_key(h) for h in reader.fieldnames]

#         for raw_row in reader:
#             row = {clean_key(k): v for k, v in raw_row.items()}

#             product = get_fk(Product, row.get('product_id'))
#             branch = get_fk(Branch, row.get('branch_id'))

#             if not product or not branch:
#                 continue

#             # barcode unique hai – duplicate avoid
#             if Stock.objects.filter(barcode=row.get('barcode')).exists():
#                 print(f"⚠️ Already exists: {row.get('barcode')}")
#                 continue

#             stock = Stock(
#                 product=product,
#                 branch=branch,
#                 qty=int(row.get('stock') or 0),
#                 barcode=row.get('barcode')
#             )

#             stocks.append(stock)

#     Stock.objects.bulk_create(stocks)
#     print(f"✅ {len(stocks)} stock rows imported successfully!")


# if __name__ == "__main__":
#     run()


import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
django.setup()

from vendor.models import PurchaseItem, StockIn
from product.models import Stock
from company.models import Branch
from product.models import Product

CSV_FILE_PATH = 'data/quantity.csv'


def clean_key(key):
    return key.replace('\ufeff', '').strip().lower()


def run():
    with open(CSV_FILE_PATH, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [clean_key(h) for h in reader.fieldnames]

        for raw_row in reader:
            row = {clean_key(k): v for k, v in raw_row.items()}

            product_id = int(row['product_id'])
            branch_id = int(row['branch_id'])
            qty = int(row['stock'])

            try:
                product = Product.objects.get(id=product_id)
                branch = Branch.objects.get(id=branch_id)
            except Exception as e:
                print(f"❌ Invalid product/branch: {e}")
                continue

            # 🔥 PurchaseItem fetch using product_id
            purchase_items = PurchaseItem.objects.filter(product=product)

            if not purchase_items.exists():
                print(f"⚠️ No purchase item found for product {product_id}")
                continue

            for item in purchase_items:

                # 1️⃣ Stock (current)
                stock, created = Stock.objects.get_or_create(
                    product=item.product,
                    variant=item.variant,
                    branch=branch,
                    defaults={'qty': 0}
                )

                stock.qty += qty
                stock.save()

                # 2️⃣ StockIn (history)
                StockIn.objects.create(
                    purchase=item.purchase,
                    purchase_item=item,
                    product=item.product,
                    variant=item.variant,
                    branch=branch,
                    qty=qty
                )

                print(
                    f"✅ Product {product.id} | Branch {branch.id} | "
                    f"Qty {qty} | PurchaseItem {item.id}"
                )


if __name__ == "__main__":
    run()
