# import os
# import django
# import csv

# # 🔥 Django setup
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
# django.setup()

# from company.models import Company

# CSV_FILE_PATH = 'data/company.csv'   # agar alag jagah hai to path change kar

# def run():
#     with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)

#         for row in reader:
#             Company.objects.create(
#                 **row   # 🔥 column name same hai isliye direct
#             )

#     print("✅ Company data successfully imported!")

# if __name__ == "__main__":
#     run()

# import os
# import django
# import csv

# # 🔥 Django setup
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
# django.setup()

# from company.models import Branch

# CSV_FILE_PATH = 'data/branch.csv'

# def run():
#     with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)

#         objs = []

#         for row in reader:
#             objs.append(Branch(**row))  # 🔥 id ke saath object

#         Branch.objects.bulk_create(objs)
#         print("✅ Branch data successfully imported with IDs!")

# if __name__ == "__main__":
#     run()



# import os
# import django
# import csv

# # 🔥 Django setup
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
# django.setup()

# from product.models import Commission

# CSV_FILE_PATH = 'data/comission.csv'

# def run():
#     objs = []

#     with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)

#         for row in reader:
#             objs.append(Commission(**row))  # 🔥 direct mapping

#     Commission.objects.bulk_create(objs)
#     print("✅ Commission data successfully imported!")

# if __name__ == "__main__":
#     run()

# import os
# import django
# import csv

# # 🔥 Django setup
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
# django.setup()

# from product.models import Category, Commission

# CSV_FILE_PATH = 'data/category.csv'

# def run():
#     objs = []

#     with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)

#         for row in reader:
#             commission_id = row.pop('commission_id')  # 🔥 FK alag nikala

#             try:
#                 commission_obj = Commission.objects.get(id=commission_id)
#             except Commission.DoesNotExist:
#                 print(f"❌ Commission not found for ID: {commission_id}")
#                 continue

#             objs.append(
#                 Category(
#                     commission=commission_obj,
#                     **row
#                 )
#             )

#     Category.objects.bulk_create(objs)
#     print("✅ Category data successfully imported!")

# if __name__ == "__main__":
#     run()


# import os
# import django
# import csv

# # 🔥 Django setup
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
# django.setup()

# from product.models import SubCategory

# CSV_FILE_PATH = 'data/subcategory.csv'

# def run():
#     objs = []

#     with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)

#         for row in reader:
#             # id + category_id dono CSV se aa rahe hain
#             objs.append(SubCategory(**row))

#     SubCategory.objects.bulk_create(objs)
#     print("✅ SubCategory data successfully imported with IDs!")

# if __name__ == "__main__":
#     run()


# import os
# import django
# import csv

# # 🔥 Django setup
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
# django.setup()

# from product.models import HSN, Category

# CSV_FILE_PATH = 'data/hsn.csv'

# def run():
#     objs = []

#     with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)

#         for row in reader:
#             category_id = row.pop('category_id')  # FK alag nikala

#             try:
#                 category_obj = Category.objects.get(id=category_id)
#             except Category.DoesNotExist:
#                 print(f"❌ Category not found for ID: {category_id}")
#                 continue

#             objs.append(
#                 HSN(
#                     category=category_obj,  # ✅ FK resolved
#                     **row
#                 )
#             )

#     HSN.objects.bulk_create(objs)
#     print("✅ HSN data successfully imported with Category FK!")

# if __name__ == "__main__":
#     run()


# import os
# import django
# import csv

# # 🔥 Django setup
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
# django.setup()

# from product.models import Brand, Category

# CSV_FILE_PATH = 'data/brand.csv'

# def run():
#     objs = []

#     with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)

#         for row in reader:
#             category_id = row.pop('category_id')  # FK alag nikala

#             try:
#                 category_obj = Category.objects.get(id=category_id)
#             except Category.DoesNotExist:
#                 print(f"❌ Category not found for ID: {category_id}")
#                 continue

#             objs.append(
#                 Brand(
#                     category=category_obj,  # ✅ FK set
#                     **row
#                 )
#             )

#     Brand.objects.bulk_create(objs)
#     print("✅ Brand data successfully imported with Category FK!")

# if __name__ == "__main__":
#     run()


import os
import django
import csv

# 🔥 Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gf_backend.settings')
django.setup()

from vendor.models import Vendor

CSV_FILE_PATH = 'data/vendor.csv'

def run():
    objs = []

    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            objs.append(Vendor(**row))  # 🔥 direct import (id + fields)

    Vendor.objects.bulk_create(objs)
    print("✅ Vendor data successfully imported!")

if __name__ == "__main__":
    run()
