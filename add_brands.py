import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gf_backend.settings")
django.setup()

from product.models import Brand, Category


BRANDS = [
    "APPLE",
    "SAMSUNG",
    "JTP",
    "GOLDFIRE",
    "LUNE",
    "BASEUS",
    "LITO",
    "XUNDO",
    "BULEO",
    "REMIX",
    "WOPOW",
    "RIVANO",
]

CATEGORY_START_ID = 3
CATEGORY_END_ID = 19


def run():
    categories = Category.objects.filter(
        id__gte=CATEGORY_START_ID,
        id__lte=CATEGORY_END_ID
    )

    if not categories.exists():
        print("❌ No categories found between 3 and 19")
        return

    for category in categories:
        print(f"\n📂 Category ID: {category.id} ({category.name})")

        for brand_name in BRANDS:
            brand_name = brand_name.strip().upper()

            obj, created = Brand.objects.get_or_create(
                name=brand_name,
                category=category
            )

            if created:
                print(f"  ✅ Added: {brand_name}")
            else:
                print(f"  ℹ️ Already exists: {brand_name}")


if __name__ == "__main__":
    run()
