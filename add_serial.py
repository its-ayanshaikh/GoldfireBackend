import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
django.setup()

from product.models import Product, SerialNumber
from vendor.models import PurchaseItem

CSV_FILE_PATH = 'data/serial.csv'


def clean_key(key):
    return key.replace('\ufeff', '').strip().lower()


def get_product_purchase_item(product):
    """
    Since each product has only ONE purchase item currently
    """
    purchase_item = PurchaseItem.objects.filter(product=product).first()
    if not purchase_item:
        print(f"❌ PurchaseItem not found for product {product.id}")
    return purchase_item


def run():
    serials = []

    with open(CSV_FILE_PATH, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [clean_key(h) for h in reader.fieldnames]

        for raw_row in reader:
            row = {clean_key(k): v for k, v in raw_row.items()}

            product_id = row.get('product_id')
            serial_number = str(row.get('serial_number')).strip()

            if not product_id or not serial_number:
                continue

            try:
                product = Product.objects.get(id=int(product_id))
            except Product.DoesNotExist:
                print(f"❌ Product not found id={product_id}")
                continue

            purchase_item = get_product_purchase_item(product)
            if not purchase_item:
                continue

            serial = SerialNumber(
                purchase_item=purchase_item,
                product=product,
                serial_number=serial_number,
                is_available=True if str(row.get('is_available')) == '1' else False
            )

            serials.append(serial)

    SerialNumber.objects.bulk_create(serials)
    print(f"✅ {len(serials)} serial numbers imported successfully!")


if __name__ == "__main__":
    run()
