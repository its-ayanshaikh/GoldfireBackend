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
@parser_classes([MultiPartParser, FormParser])
def create_purchase(request):
    """
    Create a new purchase entry with multiple optional receipt files.
    Expected fields:
      - vendor (int)
      - total (decimal)
      - purchase_date (YYYY-MM-DD)
      - notes (optional)
      - receipt_files[] (multiple files optional)
    """
    try:
        vendor_id = request.data.get("vendor")
        total = request.data.get("total")
        purchase_date = request.data.get("purchase_date")
        notes = request.data.get("notes")

        if not vendor_id or not total or not purchase_date:
            return Response(
                {"error": "vendor, total, and purchase_date are required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate vendor
        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"error": "Invalid vendor ID."}, status=status.HTTP_404_NOT_FOUND)

        # Create Purchase record
        purchase = Purchase.objects.create(
            vendor=vendor,
            total=total,
            purchase_date=purchase_date,
            notes=notes
        )

        # Handle multiple receipt files
        receipt_files = request.FILES.getlist("receipt_files")
        for file in receipt_files:
            PurchaseReceipt.objects.create(purchase=purchase, file=file)

        serializer = PurchaseSerializer(purchase)
        return Response(
            {"message": "Purchase added successfully."},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# List All Purchases 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_purchases(request):
    """
    Get all purchases with multiple receipts and vendor details.
    """
    try:
        # Optimize DB queries (select_related + prefetch_related)
        purchases = (
            Purchase.objects
            .select_related('vendor')
            .prefetch_related('receipts')
            .all()
            .order_by('-purchase_date')
        )

        serializer = PurchaseSerializer(purchases, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
