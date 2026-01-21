from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import CategorySerializer, SubCategorySerializer, BrandSerializer, ModelSerializer, SubBrandSerializer, TypeSerializer, HSNSerializer, ProductSerializer, QuantitySerializer, CommissionSerializer
from django.db import transaction
from .utils import generate_barcode_text
from django.db.models import Q
from django.core.exceptions import ValidationError
from employee.pagination import EmployeePagination

# ------------------------
# LIST CATEGORIES
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    """
    Fetch all categories
    """
    categories = Category.objects.all().order_by('id')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ------------------------
# CATEGORY COMMISSION
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_category_commission(request, category_id):
    try:
        category = Category.objects.select_related("commission").get(id=category_id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    commission = category.commission

    return Response({
        "category_id": category.id,
        "commission_type": commission.commission_type if commission else None,
        "commission_value": commission.commission_value if commission else None
    })

# ------------------------
# LIST COMMISSION CATEGORIES
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def commission_categories(request):
    """
    Fetch all categories who has no commission assigned
    """
    categories = Category.objects.filter(commission__isnull=True).order_by('id')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ------------------------
# LIST COMMISSION
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def commission_list(request):
    try:
        commissions = Commission.objects.all()
        serializer = CommissionSerializer(commissions, many=True)
        return Response(serializer.data)

    except Exception as e:
        return Response(
            {"error": "Something went wrong while fetching commission list", "details": str(e)},
            status=500
        )
     
# ------------------------
# CREATE COMMISSION
# ------------------------   
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def commission_create(request):
    try:
        serializer = CommissionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Create Commission
        commission = Commission.objects.create(
            name=serializer.validated_data['name'],
            commission_type=serializer.validated_data['commission_type'],
            commission_value=serializer.validated_data['commission_value']
        )

        # Assign categories
        category_ids = serializer.validated_data.get("categories", [])
        try:
            Category.objects.filter(id__in=category_ids).update(commission=commission)
        except Exception as e:
            commission.delete()  # rollback
            return Response(
                {"error": "Invalid category IDs", "details": str(e)},
                status=400
            )

        return Response(CommissionSerializer(commission).data, status=201)

    except Exception as e:
        return Response(
            {"error": "Failed to create commission", "details": str(e)},
            status=500
        )

# ------------------------
# UPDATE COMMISSION
# ------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def commission_update(request, pk):
    try:
        commission = Commission.objects.get(pk=pk)
    except Commission.DoesNotExist:
        return Response({"error": "Commission not found"}, status=404)

    try:
        serializer = CommissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Update main fields
        commission.name = serializer.validated_data['name']
        commission.commission_type = serializer.validated_data['commission_type']
        commission.commission_value = serializer.validated_data['commission_value']
        commission.save()

        # Update category assignment
        category_ids = serializer.validated_data.get("categories", [])

        try:
            # old categories ko remove karega
            Category.objects.filter(commission=commission).update(commission=None)

            # new assign karega
            Category.objects.filter(id__in=category_ids).update(commission=commission)

        except Exception as e:
            return Response(
                {"error": "Failed to update category assignment", "details": str(e)},
                status=400
            )

        return Response(CommissionSerializer(commission).data)

    except Exception as e:
        return Response(
            {"error": "Failed to update commission", "details": str(e)},
            status=500
        )


# ------------------------
# DELETE COMMISSION
# ------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def commission_delete(request, pk):
    try:
        commission = Commission.objects.get(pk=pk)
    except Commission.DoesNotExist:
        return Response({"error": "Commission not found"}, status=404)

    try:
        # remove commission from categories first
        Category.objects.filter(commission=commission).update(commission=None)

        commission.delete()

        return Response({"message": "Commission deleted successfully"}, status=200)

    except Exception as e:
        return Response(
            {"error": "Failed to delete commission", "details": str(e)},
            status=500
        )


# ------------------------
# CREATE HSN
# ------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_hsn(request):
    serializer = HSNSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------
# LIST HSN (Category-wise or All)
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_hsn(request):
    category_id = request.query_params.get('category_id', None)
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            hsn_codes = HSN.objects.filter(category=category).select_related('category').order_by('id')
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        hsn_codes = HSN.objects.select_related('category').order_by('id')

    serializer = HSNSerializer(hsn_codes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ------------------------
# UPDATE HSN
# ------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_hsn(request, hsn_id):
    try:
        hsn = HSN.objects.get(id=hsn_id)
    except HSN.DoesNotExist:
        return Response({'error': 'HSN not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = HSNSerializer(hsn, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------
# DELETE HSN
# ------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_hsn(request, hsn_id):
    try:
        hsn = HSN.objects.get(id=hsn_id)
    except HSN.DoesNotExist:
        return Response({'error': 'HSN not found'}, status=status.HTTP_404_NOT_FOUND)

    hsn.delete()
    return Response({'message': 'HSN deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# ------------------------
# CREATE SUBCATEGORY
# ------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subcategory(request):
    serializer = SubCategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------- LIST ----------
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def list_subcategories(request):
#     subcategories = SubCategory.objects.select_related('category').all().order_by('-id')
#     serializer = SubCategorySerializer(subcategories, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


# ------------------------
# UPDATE SUBCATEGORY
# ------------------------
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_subcategory(request, pk):
    try:
        subcategory = SubCategory.objects.get(pk=pk)
    except SubCategory.DoesNotExist:
        return Response({"error": "SubCategory not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = SubCategorySerializer(subcategory, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------
# DELETE SUBCATEGORY
# ------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_subcategory(request, pk):
    try:
        subcategory = SubCategory.objects.get(pk=pk)
    except SubCategory.DoesNotExist:
        return Response({"error": "SubCategory not found"}, status=status.HTTP_404_NOT_FOUND)

    subcategory.delete()
    return Response({"message": "SubCategory deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ------------------------
# GET SUBCATEGORIES BY CATEGORY
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subcategories_by_category(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    subcategories = SubCategory.objects.filter(category=category)
    serializer = SubCategorySerializer(subcategories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# ------------------------
# CREATE TYPE
# ------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_type(request):
    serializer = TypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------
# LIST TYPES (category-wise)
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_types(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    types = Type.objects.filter(category=category).select_related('category').order_by('id')
    serializer = TypeSerializer(types, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ------------------------
# UPDATE TYPE
# ------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_type(request, type_id):
    try:
        type_obj = Type.objects.get(id=type_id)
    except Type.DoesNotExist:
        return Response({'error': 'Type not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TypeSerializer(type_obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------
# DELETE TYPE
# ------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_type(request, type_id):
    try:
        type_obj = Type.objects.get(id=type_id)
    except Type.DoesNotExist:
        return Response({'error': 'Type not found'}, status=status.HTTP_404_NOT_FOUND)

    type_obj.delete()
    return Response({'message': 'Type deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# ------------------------
# CREATE BRAND
# ------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_brand(request):
    serializer = BrandSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Brand created successfully', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)


# ------------------------
# LIST ALL BRANDS
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_brands(request):
    brands = Brand.objects.select_related('category', 'subcategory').all().order_by('id')
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data, status=200)


# ------------------------
# GET BRANDS BY CATEGORY
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def brands_by_category(request, category_id):
    brands = Brand.objects.filter(category_id=category_id)
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data, status=200)


# ------------------------
# GET BRANDS BY SUBCATEGORY
# ------------------------
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def brands_by_subcategory(request, subcategory_id):
#     brands = Brand.objects.filter(subcategory_id=subcategory_id)
#     serializer = BrandSerializer(brands, many=True)
#     return Response(serializer.data, status=200)


# ------------------------
# UPDATE BRAND
# ------------------------
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_brand(request, brand_id):
    try:
        brand = Brand.objects.get(id=brand_id)
    except Brand.DoesNotExist:
        return Response({'error': 'Brand not found'}, status=404)

    serializer = BrandSerializer(brand, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Brand updated successfully', 'data': serializer.data}, status=200)
    return Response(serializer.errors, status=400)


# ------------------------
# DELETE BRAND
# ------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_brand(request, brand_id):
    try:
        brand = Brand.objects.get(id=brand_id)
    except Brand.DoesNotExist:
        return Response({'error': 'Brand not found'}, status=404)

    brand.delete()
    return Response({'message': 'Brand deleted successfully'}, status=200)


# ------------------------
# CREATE SUBBRAND
# ------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subbrand(request):
    serializer = SubBrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------
# LIST SUBBRANDS (subcategory-wise)
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_subbrands(request, subcategory_id):
    try:
        subcategory = SubCategory.objects.get(id=subcategory_id)
    except SubCategory.DoesNotExist:
        return Response({'error': 'SubCategory not found'}, status=status.HTTP_404_NOT_FOUND)

    subbrands = SubBrand.objects.filter(subcategory=subcategory).select_related('category', 'subcategory').order_by('id')
    serializer = SubBrandSerializer(subbrands, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ------------------------
# UPDATE SUBBRAND
# ------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_subbrand(request, subbrand_id):
    try:
        subbrand = SubBrand.objects.get(id=subbrand_id)
    except SubBrand.DoesNotExist:
        return Response({'error': 'SubBrand not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = SubBrandSerializer(subbrand, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------
# DELETE SUBBRAND
# ------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_subbrand(request, subbrand_id):
    try:
        subbrand = SubBrand.objects.get(id=subbrand_id)
    except SubBrand.DoesNotExist:
        return Response({'error': 'SubBrand not found'}, status=status.HTTP_404_NOT_FOUND)

    subbrand.delete()
    return Response({'message': 'SubBrand deleted successfully'}, status=status.HTTP_204_NO_CONTENT)




# ------------------------
# CREATE MODEL
# ------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_model(request):
    serializer = ModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Model created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------
# LIST ALL MODELS
# (optional filter by brand)
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_models(request, subbrand_id):
    # Check if brand exists
    try:
        subbrand = SubBrand.objects.get(id=subbrand_id)
    except Brand.DoesNotExist:
        return Response({'error': 'Brand not found'}, status=status.HTTP_404_NOT_FOUND)

    # Fetch all models under this subbrand
    models_qs = Model.objects.filter(subbrand=subbrand).select_related('subbrand', 'subbrand__category', 'subbrand__subcategory')
    


    serializer = ModelSerializer(models_qs, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)



# ------------------------
# UPDATE MODEL
# ------------------------
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_model(request, pk):
    try:
        model = Model.objects.get(pk=pk)
    except Model.DoesNotExist:
        return Response({'error': 'Model not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ModelSerializer(model, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Model updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------
# DELETE MODEL
# ------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_model(request, pk):
    try:
        model = Model.objects.get(pk=pk)
    except Model.DoesNotExist:
        return Response({'error': 'Model not found'}, status=status.HTTP_404_NOT_FOUND)

    model.delete()
    return Response({'message': 'Model deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# ------------------------
# CREATE PRODUCT
# ------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def create_product(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        product = serializer.save()
        quantities_data = request.data.get('quantities', [])
        response_data = []
        total_qty = 0

        # Barcode sequence counter
        barcode_counter = Product.objects.count() + 1

        if isinstance(quantities_data, list):
            for q in quantities_data:
                branch_id = q.get('branch')
                qty = int(q.get('qty', 0))

                if not branch_id:
                    continue

                branch = Branch.objects.get(id=branch_id)

                # ---------- Generate Barcode Text ----------
                barcode_text = generate_barcode_text(product.category, barcode_counter)
                barcode_counter += 1

                # ---------- Save Quantity ----------
                Quantity.objects.create(
                    product=product,
                    branch=branch,
                    qty=qty,
                    barcode=barcode_text  # ✅ store only text
                )

                total_qty += qty

                # ---------- Prepare Response ----------
                response_data.append({
                    "branch": branch.name,
                    "qty": qty,
                    "barcode": barcode_text,   # ✅ only text now
                    "price": float(product.selling_price)
                })

        # ---------- Handle Serial Numbers (for warranty items) ----------
        serial_numbers_data = request.data.get('serial_numbers', [])
        if product.is_warranty_item:
            if not serial_numbers_data:
                return Response(
                    {"message": "Serial numbers are required for warranty items."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if total_qty and len(serial_numbers_data) != total_qty:
                return Response(
                    {"message": f"Serial numbers count ({len(serial_numbers_data)}) must match total quantity ({total_qty})."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            for sn in serial_numbers_data:
                SerialNumber.objects.create(product=product, serial_number=sn)

        return Response({
            "product": ProductSerializer(product).data,
            "barcodes": response_data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ------------------------
# LIST PRODUCTS (Category-wise optional)
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_products(request):
    try:
        category_id = request.query_params.get('category')
        search = request.query_params.get('search')
        branch_id = request.query_params.get('branch')

        queryset = Product.objects.select_related(
            'category', 'subcategory', 'brand', 'subbrand',
            'model', 'type', 'vendor', 'hsn'
        ).prefetch_related(
            'quantities', 'quantities__branch'
        ).order_by('id')

        # ✅ Category filter
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # ✅ Search (product, model, category, branch)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(model__name__icontains=search) |
                Q(category__name__icontains=search) |
                Q(quantities__branch__name__icontains=search)
            ).distinct()

        # ✅ Branch filter
        if branch_id:
            queryset = queryset.filter(quantities__branch_id=branch_id)

        # ✅ Pagination
        paginator = EmployeePagination()
        paginated_qs = paginator.paginate_queryset(queryset, request)

        serializer = ProductSerializer(paginated_qs, many=True)
        print(serializer.data)
        return paginator.get_paginated_response(serializer.data)

    except ValidationError as e:
        return Response(
            {
                "success": False,
                "message": "Invalid input data",
                "errors": e.message_dict if hasattr(e, 'message_dict') else str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        return Response(
            {
                "success": False,
                "message": "Something went wrong while fetching products",
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def remove_nulls(data):
    return {
        k: v for k, v in data.items()
        if v is not None and v != ""
    }



# ------------------------
# UPDATE PRODUCT
# ------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def update_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    print(request.data)
    cleaned_data = remove_nulls(request.data)

    serializer = ProductSerializer(
        product,
        data=cleaned_data,
        partial=True   # 🔥 IMPORTANT
    )

    if serializer.is_valid():
        product = serializer.save()

        # 🔥 SERIAL NUMBER UPDATE / ADD
        serial_numbers = cleaned_data.get('serial_numbers', [])
        
        # Quantity update (only if quantities sent)
        quantities_data = cleaned_data.get('quantities', [])
        
        for q in quantities_data:
            if q.get('branch') is not None:
                quantity_obj, created = Quantity.objects.update_or_create(
                        product=product,
                        branch_id=branch_id,
                        defaults={'qty': qty}
                )

                # ✅ Barcode sirf tab generate hoga jab naya Quantity create ho
                if created:
                    barcode_text = generate_barcode_text(product.category, barcode_counter)
                    barcode_counter += 1

                    quantity_obj.barcode = barcode_text
                    quantity_obj.save()
                

        if product.is_warranty_item and serial_numbers:
            existing_serial_number = product.serial_numbers.all()
            existing_serial_number.delete()  # delete existing serial numbers
            
            for sn in serial_numbers:
                SerialNumber.objects.create(
                    product=product,
                    serial_number=sn,
                    is_available=True
                )


        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ------------------------
# DELETE PRODUCT
# ------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    product.delete()
    return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
