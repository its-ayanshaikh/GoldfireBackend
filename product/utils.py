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
