import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
django.setup()

from product.models import Product, Category, SubCategory, Brand, Type, HSN

CSV_FILE_PATH = 'data/product_master.csv'


def clean_key(key):
    """ remove BOM, spaces, lowercase """
    return key.replace('\ufeff', '').strip().lower()


def get_fk(model, value):
    if not value or str(value).strip() in ('0', ''):
        return None
    try:
        return model.objects.get(id=int(value))
    except model.DoesNotExist:
        print(f"❌ FK not found: {model.__name__} id={value}")
        return None


def run():
    products = []

    with open(CSV_FILE_PATH, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        # 🔥 normalize headers
        reader.fieldnames = [clean_key(h) for h in reader.fieldnames]

        for raw_row in reader:
            row = {clean_key(k): v for k, v in raw_row.items()}

            product = Product(
                id=int(row['id']),
                name=row.get('name'),

                category=get_fk(Category, row.get('category_id')),
                subcategory=get_fk(SubCategory, row.get('subcategory_id')),
                brand=get_fk(Brand, row.get('brand_id')),
                type=get_fk(Type, row.get('type_id')),
                hsn=get_fk(HSN, row.get('hsn_id')),

                commission_type=row.get('commission_type'),
                commission_value=row.get('commission_value') or None,

                status=row.get('status'),

                selling_price=row.get('selling_price'),
                minimum_selling_price=row.get('min_selling_price'),
                minimum_quantity=row.get('min_qty_alert') or 1,

                is_warranty_item=True if str(row.get('is_warranty_item')) == '1' else False,
                warranty_period=row.get('warranty_period') or None,
            )

            products.append(product)

    Product.objects.bulk_create(products)
    print(f"✅ {len(products)} products imported successfully!")


if __name__ == "__main__":
    run()
