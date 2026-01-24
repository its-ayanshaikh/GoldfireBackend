from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from employee.pagination import EmployeePagination
import re
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
from rest_framework.parsers import MultiPartParser, FormParser
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from django.db import transaction
from rest_framework import status
from django.db import IntegrityError
from product.models import Product, ProductVariant, Stock
from django.shortcuts import get_object_or_404
import json
from company.models import *

# List Vendors
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_vendors(request):
    """
    List all vendors
    """
    vendors = Vendor.objects.all().order_by('-created_at')
    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Create Vendor
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vendor(request):
    """
    Create a new vendor
    """
    serializer = VendorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Vendor
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_vendor(request, pk):
    """
    Update an existing vendor
    """
    try:
        vendor = Vendor.objects.get(id=pk)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = VendorSerializer(vendor, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete Vendor
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_vendor(request, pk):
    """
    Delete a vendor by ID
    """
    try:
        vendor = Vendor.objects.get(id=pk)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    vendor.delete()
    return Response({"message": "Vendor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# OCR and Data Extraction for Purchase Receipts
# def extract_total_and_date_from_text(text):
#     """
#     Improved OCR parser for receipts — handles fuzzy DT/DATE text, 2-digit years,
#     varied punctuation, and ₹ symbols.
#     """

#     # Normalize text
#     clean_text = text.replace("\n", " ").replace("₹", "").upper()
#     clean_text = re.sub(r"\s+", " ", clean_text)

#     # DATE PATTERN (very flexible now)
#     # Handles: DT : 04/10/25, DATE 04-10-25, OT + 04/40/25, etc.
#     date_pattern = r'(?:D[TAE]{1,2}|OT|0T|DA|DTE|DATE)\s*[:\-\+\.\s]?\s*(\d{1,2}[\/\-\.\s]\d{1,2}[\/\-\.\s]\d{2,4})'

#     # TOTAL PATTERN (covers GRAND TOTAL, AMOUNT, T0TAL etc.)
#     total_pattern = r'(?:GR[A-Z0-9]{0,3}\s*TOT[A-Z0-9]{0,3}|TOT[A-Z0-9]{0,3}|AMOUNT)\D{0,8}(\d{1,3}(?:[,\d{3}]*)?(?:\.\d{1,2})?)'

#     # Try to extract date
#     date_match = re.search(date_pattern, clean_text)
#     found_date = date_match.group(1).replace(" ", "") if date_match else None

#     # Try to extract total (take last occurrence)
#     total_matches = re.findall(total_pattern, clean_text)
#     found_total = total_matches[-1].replace(",", "") if total_matches else None

#     # If total still not found → fallback to large numeric value (≥4 digits)
#     if not found_total:
#         number_candidates = re.findall(r'\b\d{4,6}(?:\.\d{1,2})?\b', clean_text)
#         if number_candidates:
#             found_total = number_candidates[-1]
            
#     return found_total, found_date

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])
# def extract_purchase_data(request):
#     """
#     Upload image/PDF file → OCR → return extracted total and date
#     """
#     file = request.FILES.get('file')

#     if not file:
#         return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         # Case 1: Image file
#         if file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
#             image = Image.open(file)
#             text = pytesseract.image_to_string(image)

#         # Case 2: PDF file
#         elif file.name.lower().endswith('.pdf'):
#             pages = convert_from_bytes(file.read())
#             text = ""
#             for page in pages:
#                 text += pytesseract.image_to_string(page)
#         else:
#             return Response({"error": "Unsupported file format. Upload PDF or Image."},
#                             status=status.HTTP_400_BAD_REQUEST)

#         total, purchase_date = extract_total_and_date_from_text(text)

#         print(purchase_date)
#         return Response({
#             "message": "OCR extraction successful.",
#             "purchase_date": purchase_date,
#             "total": total,
#         }, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Add Purchase CRUD views similarly if needed
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_purchase(request):

    try:
        print(request.data)
        with transaction.atomic():

            # 1️⃣ Purchase
            purchase = Purchase.objects.create(
                vendor_id=request.data.get('vendor'),
                bill_no=request.data.get('bill_no'),
                purchase_date=request.data.get('purchase_date'),
                notes=request.data.get('notes'),
                total=0
            )

            items = json.loads(request.data.get('items', '[]'))
            receipts = request.FILES.getlist('receipts')

            grand_total = 0
            barcode_counter = Stock.objects.count() + 1
            created_items = []
            
            # 2️⃣ Items + Branch-wise Stock
            for item in items:
                product = Product.objects.get(id=item['product'])
                variant = None

                if item.get('variant'):
                    variant = ProductVariant.objects.get(id=item['variant'])

                selling_price = (
                    variant.selling_price
                    if variant and variant.selling_price
                    else product.selling_price
                )

                purchase_price = float(item['purchase_price'])

                total_qty = sum(b['qty'] for b in item['branches'])
                item_total = total_qty * purchase_price

                barcode = generate_barcode_text(product.category, barcode_counter)
                barcode_counter += 1
                
                purchase_item = PurchaseItem.objects.create(
                    purchase=purchase,
                    product=product,
                    variant=variant,
                    qty=total_qty,
                    purchase_price=purchase_price,
                    selling_price=selling_price,
                    total=item_total,
                    barcode=barcode
                )
                
                created_items.append({
                    "purchase_item_id": purchase_item.id,
                    "product_id": product.id,
                    "product_name": product.name,
                    "variant": (
                        {
                            "id": variant.id,
                            "name": str(variant)
                        } if variant else None
                    ),
                    "barcode": purchase_item.barcode,
                    "selling_price": float(purchase_item.selling_price),
                    "qty": total_qty
                })


                grand_total += item_total

                # 📦 STOCK (branch-wise)
                for b in item['branches']:
                    branch = Branch.objects.get(id=b['branch'])
                    qty = int(b['qty'])

                    if variant:
                        stock, created = Stock.objects.get_or_create(
                            product=product,
                            variant=variant,
                            branch=branch,
                            defaults={
                                "qty": qty,
                            }
                        )
                    else:
                        stock, created = Stock.objects.get_or_create(
                            product=product,
                            variant=None,   # important
                            branch=branch,
                            defaults={
                                "qty": qty,
                            }
                        )
                        
                    # 2️⃣ Stock history save
                    StockIn.objects.create(
                        purchase=purchase,
                        purchase_item=purchase_item,
                        product=product,
                        variant=variant,
                        branch=branch,
                        qty=qty
                    )
                        
                    stock.qty = qty
                    stock.save(update_fields=["qty"])

                # 🔢 SERIAL NUMBERS (ONLY WARRANTY ITEMS)
                if product.is_warranty_item:
                    serials = item.get('serial_numbers', [])

                    if len(serials) != total_qty:
                        raise ValueError(
                            f"Serial numbers count mismatch for product {product.id}"
                        )

                    for sn in serials:
                        SerialNumber.objects.create(
                            purchase_item=purchase_item,
                            product=product,
                            variant=variant,
                            serial_number=sn,
                            is_available=True
                        )

            # 3️⃣ Receipts
            for file in receipts:
                PurchaseReceipt.objects.create(
                    purchase=purchase,
                    file=file
                )

            # 4️⃣ Update Purchase Total
            purchase.total = grand_total
            purchase.save()

            return Response({
                "success": True,
                "message": "Purchase created with branch-wise stock & serial numbers",
                "purchase_id": purchase.id,
                "items": created_items 
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(e)
        return Response({
            "success": False,
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
        
        

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_purchase(request, pk):
    try:
        with transaction.atomic():
            # 🔒 1️⃣ LOCK PURCHASE
            purchase = Purchase.objects.select_for_update().get(id=pk)

            receipts = request.FILES.getlist('receipts')
            for file in receipts:
                PurchaseReceipt.objects.create(
                    purchase=purchase,
                    file=file
                )
            
            # ❌ If any serial already used → HARD LOCK
            if SerialNumber.objects.filter(
                purchase_item__purchase=purchase,
                is_available=False
            ).exists():
                return Response({
                    "success": False,
                    "error": "Purchase locked. Some serial numbers already used."
                }, status=400)

            # ❌ If stock already consumed → HARD LOCK
            for item in purchase.items.all():
                total_in_qty = StockIn.objects.filter(
                    purchase_item=item
                ).aggregate(total=models.Sum('qty'))['total'] or 0

                if total_in_qty < item.qty:
                    return Response({
                        "success": False,
                        "error": "Purchase locked. Stock already consumed."
                    }, status=400)



            # 📥 INPUT
            items = json.loads(request.data.get('items', '[]'))

            # =====================================================
            # 🧠 2️⃣ PURE VALIDATION (NO DB WRITE)
            # =====================================================

            for item in items:
                product = Product.objects.get(id=item['product'])
                variant = (
                    ProductVariant.objects.get(id=item['variant'])
                    if item.get('variant') else None
                )

                total_qty = sum(int(b['qty']) for b in item['branches'])

                if product.is_warranty_item:
                    incoming_serials = item.get('serial_numbers', [])

                    # ❌ qty mismatch
                    if len(incoming_serials) != total_qty:
                        return Response({
                            "success": False,
                            "error": f"Serial count mismatch for {product.name}"
                        }, status=400)

            # =====================================================
            # 🔄 3️⃣ UPDATE PURCHASE BASIC INFO
            # =====================================================

            purchase.vendor_id = request.data.get('vendor')
            purchase.bill_no = request.data.get('bill_no')
            purchase.purchase_date = request.data.get('purchase_date')
            purchase.notes = request.data.get('notes')
            purchase.save()

            # =====================================================
            # 🔁 4️⃣ OLD ITEMS MAP
            # =====================================================

            old_items = {
                (i.product_id, i.variant_id): i
                for i in purchase.items.all()
            }

            new_total = 0

            # =========================
            # 🔥 DELETE OLD STOCK-IN (RESET HISTORY)
            # =========================
            StockIn.objects.filter(purchase=purchase).delete()
            
            # =====================================================
            # 📦 5️⃣ ITEMS + STOCK UPDATE
            # =====================================================

            for item in items:
                product = Product.objects.get(id=item['product'])
                variant = (
                    ProductVariant.objects.get(id=item['variant'])
                    if item.get('variant') else None
                )

                purchase_price = float(item['purchase_price'])
                total_qty = sum(int(b['qty']) for b in item['branches'])
                total = total_qty * purchase_price

                key = (product.id, variant.id if variant else None)

                # 🔄 UPDATE OR CREATE ITEM
                purchase_item = old_items.pop(key, None)

                
                if purchase_item:
                    purchase_item.qty = total_qty
                    purchase_item.purchase_price = purchase_price
                    purchase_item.total = total
                    purchase_item.save()
                else:
                    
                    barcode = generate_barcode_text(product.category, barcode_counter)
                    barcode_counter += 1
                    
                    purchase_item = PurchaseItem.objects.create(
                        purchase=purchase,
                        product=product,
                        variant=variant,
                        qty=total_qty,
                        purchase_price=purchase_price,
                        selling_price=(
                            variant.selling_price if variant else product.selling_price
                        ),
                        total=total,
                        barcode=barcode
                    )

                new_total += total

                # =========================
                # 📦 STOCK (BRANCH WISE)
                # =========================

                existing_stocks = {
                    s.branch_id: s
                    for s in Stock.objects.filter(
                        product=product,
                        variant=variant
                    )
                }

                for b in item['branches']:
                    branch_id = b['branch']
                    qty = int(b['qty'])

                    # ======================
                    # 📦 STOCK (CURRENT)
                    # ======================
                    if branch_id in existing_stocks:
                        stock = existing_stocks.pop(branch_id)
                        stock.qty = qty
                        stock.save()
                    else:
                        Stock.objects.create(
                            product=product,
                            variant=variant,
                            branch_id=branch_id,
                            qty=qty
                        )

                    # ======================
                    # 📜 STOCK-IN (HISTORY)
                    # ======================
                    StockIn.objects.create(
                        purchase=purchase,
                        purchase_item=purchase_item,
                        product=product,
                        variant=variant,
                        branch_id=branch_id,
                        qty=qty
                    )

                # ❌ remove deleted branches stock
                for s in existing_stocks.values():
                    s.delete()


                # =========================
                # 🔢 SERIAL NUMBERS (SAFE)
                # =========================

                if product.is_warranty_item:
                    incoming_serials = set(item.get('serial_numbers', []))

                    existing_serials = {
                        s.serial_number: s
                        for s in SerialNumber.objects.filter(
                            purchase_item=purchase_item
                        )
                    }

                    # ➕ ADD NEW SERIALS
                    for sn in incoming_serials:
                        if sn not in existing_serials:
                            SerialNumber.objects.create(
                                purchase_item=purchase_item,
                                product=product,
                                variant=variant,
                                serial_number=sn,
                                is_available=True
                            )

                    # ❌ REMOVE ONLY UNUSED SERIALS
                    for sn, obj in existing_serials.items():
                        if sn not in incoming_serials and obj.is_available:
                            obj.delete()

            # =========================
            # ❌ DELETE REMOVED ITEMS
            # =========================

            for removed_item in old_items.values():
                StockIn.objects.filter(purchase_item=removed_item).delete()
                removed_item.delete()


            purchase.total = new_total
            purchase.save()

            return Response({
                "success": True,
                "message": "Purchase updated safely (serial-safe, stock-safe)"
            })

    except Exception as e:
        print(e)
        return Response({
            "success": False,
            "error": str(e)
        }, status=400)




# List All Purchases 
from django.db.models import Q
from django.utils.timezone import now

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_purchases(request):

    queryset = (
        Purchase.objects
        .select_related('vendor')
        .prefetch_related('items', 'receipts')
        .order_by('-id')
    )

    # =========================
    # 🔍 SEARCH (bill_no)
    # =========================
    search = request.query_params.get('search')
    if search:
        queryset = queryset.filter(
            bill_no__icontains=search
        )

    # =========================
    # 🏪 VENDOR FILTER
    # =========================
    vendor_id = request.query_params.get('vendor')
    if vendor_id:
        queryset = queryset.filter(vendor_id=vendor_id)

    # =========================
    # 📅 MONTH / YEAR FILTER
    # =========================
    month = request.query_params.get('month')
    year = request.query_params.get('year')

    current_year = now().year

    if month and year:
        queryset = queryset.filter(
            purchase_date__month=month,
            purchase_date__year=year
        )
    elif month:
        queryset = queryset.filter(
            purchase_date__month=month,
            purchase_date__year=current_year
        )
    elif year:
        queryset = queryset.filter(
            purchase_date__year=year
        )

    # =========================
    # 📄 PAGINATION
    # =========================
    paginator = EmployeePagination()
    page = paginator.paginate_queryset(queryset, request)

    results = []

    for p in page:
        results.append({
            "id": p.id,
            "vendor": {
                "id": p.vendor.id,
                "name": p.vendor.name
            },
            "bill_no": p.bill_no,
            "purchase_date": p.purchase_date,
            "total": float(p.total),
            "items_count": p.items.count(),
            "receipts_count": p.receipts.count(),
            "created_at": p.created_at
        })

    return paginator.get_paginated_response({
        "success": True,
        "results": results
    })

    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def purchase_detail(request, pk):

    purchase = Purchase.objects.select_related(
        'vendor'
    ).prefetch_related(
        'items__stock_ins',
        'items__serials',
        'receipts'
    ).get(id=pk)

    items_data = []

    for item in purchase.items.all():

        # 🔥 branch-wise purchased stock (from StockIn)
        stock_data = []
        for stock_in in item.stock_ins.all():
            stock_data.append({
                "branch": {
                    "id": stock_in.branch.id,
                    "name": stock_in.branch.name
                },
                "qty": stock_in.qty
            })

        # serial numbers
        serials = []
        for sn in item.serials.all():
            serials.append({
                "serial_number": sn.serial_number,
                "is_available": sn.is_available
            })

        items_data.append({
            "id": item.id,
            "product": {
                "id": item.product.id,
                "name": item.product.name,
                "is_warranty_item": item.product.is_warranty_item
            },
            "variant": (
                {
                    "id": item.variant.id,
                    "name": str(item.variant)
                } if item.variant else None
            ),
            "qty": item.qty,
            "purchase_price": float(item.purchase_price),
            "selling_price": float(item.selling_price),
            "total": float(item.total),
            "stocks": stock_data,  # 👈 ab ye StockIn se aa raha
            "serial_numbers": serials
        })

    receipts_data = []
    for r in purchase.receipts.all():
        receipts_data.append({
            "id": r.id,
            "file": r.file.url,
            "uploaded_at": r.uploaded_at
        })

    return Response({
        "success": True,
        "purchase": {
            "id": purchase.id,
            "vendor": {
                "id": purchase.vendor.id,
                "name": purchase.vendor.name
            },
            "bill_no": purchase.bill_no,
            "purchase_date": purchase.purchase_date,
            "notes": purchase.notes,
            "total": float(purchase.total),
            "items": items_data,
            "receipts": receipts_data,
            "created_at": purchase.created_at
        }
    })



# LIST ALL RETURN TO VENDOR ENTRIES (MONTHLY)
from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_return_monthly_list(request):
    try:
        params = request.query_params

        month = params.get('month')
        year = params.get('year')

        if not month or not year:
            return Response(
                {"error": "month and year are required"},
                status=400
            )

        search = params.get('search')
        branch = params.get('branch')
        vendor = params.get('vendor')
        category = params.get('category')

        queryset = VendorReturnMonthly.objects.select_related(
            'product',
            'vendor',
            'branch',
            'product__category',
            'product__brand',
            'product__model'
        ).filter(
            month=month,
            year=year
        )

        # 🔍 SEARCH
        if search:
            queryset = queryset.filter(
                Q(product__name__icontains=search) |
                Q(product__model__name__icontains=search)
            )

        # 🎛 FILTERS
        if branch:
            queryset = queryset.filter(branch_id=branch)

        if vendor:
            queryset = queryset.filter(vendor_id=vendor)

        if category:
            queryset = queryset.filter(product__category_id=category)

        queryset = queryset.order_by('product__name')

        # 📄 PAGINATION
        paginator = EmployeePagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = VendorReturnMonthlyListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=500
        )
