import datetime
import random
import string

def generate_barcode_text(category, counter):
    # CATEGORY SHORT (2 letters max for clarity)
    if category and category.name:
        cat_code = category.name[:3].upper()
    else:
        cat_code = "GN"

    # DATE (YYMM) — inventory readable
    now = datetime.datetime.now()
    yymm = now.strftime("%y%m")  # e.g. 2501

    # SMALL RANDOM CHAR (to avoid predictability)
    salt = random.choice(string.ascii_uppercase)

    # FINAL BARCODE
    return f"{cat_code}{yymm}{salt}{str(counter).zfill(4)}"


def build_display_name(product, variant=None):
    """
    Human-friendly display name for a product line.

    Many products (e.g. mobile covers) are stored with an empty `name` and
    are identified only by their category + model. For those we build a name
    like "Cover - iPhone 15" instead of showing a blank. Falls back through
    category, model, brand and finally the product id so the name is NEVER
    empty on a bill / list / search result.
    """
    if product is None:
        return ""

    name = (product.name or "").strip()
    if name:
        return name

    category_name = ""
    try:
        if product.category and product.category.name:
            category_name = product.category.name.strip()
    except Exception:
        category_name = ""

    model_name = ""
    try:
        if variant is not None and variant.model and variant.model.name:
            model_name = variant.model.name.strip()
    except Exception:
        model_name = ""

    # Fallback to the product's first variant model if no variant was given.
    if not model_name:
        try:
            first_variant = product.variants.all().first()
            if first_variant and first_variant.model and first_variant.model.name:
                model_name = first_variant.model.name.strip()
        except Exception:
            model_name = ""

    if category_name and model_name:
        return f"{category_name} - {model_name}"
    if category_name:
        return category_name
    if model_name:
        return model_name

    brand_name = ""
    try:
        if product.brand and product.brand.name:
            brand_name = product.brand.name.strip()
    except Exception:
        brand_name = ""
    if brand_name:
        return brand_name

    return f"Product #{product.id}"
