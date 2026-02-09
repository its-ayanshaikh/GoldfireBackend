from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import CategorySerializer, SubCategorySerializer, BrandSerializer, ModelSerializer, SubBrandSerializer, TypeSerializer, HSNSerializer, ProductCreateSerializer, CommissionSerializer, ProductListSerializer, ProductDetailsSerializer
from django.db import transaction
from .utils import generate_barcode_text
from django.db.models import Q
from django.core.exceptions import ValidationError
from employee.pagination import EmployeePagination
from django.db import DatabaseError
from django.db.models import Exists, OuterRef

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
        subbrands = SubBrand.objects.filter(subcategory_id=subcategory_id).order_by('id')
        serializer = SubBrandSerializer(subbrands, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except SubCategory.DoesNotExist:
        return Response({'error': 'SubCategory not found'}, status=status.HTTP_404_NOT_FOUND)


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
    models_qs = Model.objects.filter(subbrand=subbrand).select_related('subbrand')

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
    
    try:
        serializer = ProductCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product = serializer.save()

        return Response(
            {
                "message": "Product created successfully"
            },
            status=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return Response(
            {
                "message": "Something went wrong while creating product",
                "details": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ------------------------
# LIST PRODUCTS (Category-wise optional)
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_products(request):
    try:
        category_id = request.query_params.get('category')
        search = request.query_params.get('search')

        queryset = Product.objects.select_related(
            'category',
            'brand'
        ).prefetch_related(
            'variants',
            'variants__subbrand',
            'variants__model'
        ).order_by('-id')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(category__name__icontains=search) |
                Q(brand__name__icontains=search) |
                Q(variants__model__name__icontains=search)
            ).distinct()

        paginator = EmployeePagination()
        paginated_qs = paginator.paginate_queryset(queryset, request)

        serializer = ProductListSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response(
            {
                "success": False,
                "message": "Something went wrong while fetching products",
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_details(request, product_id):
    try:
        product = Product.objects.filter(id=product_id).prefetch_related(
            'variants__subbrand__subcategory',
            'variants__model'
        ).first()


        if not product:
            return Response(
                {"success": False, "message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductDetailsSerializer(product)
        return Response(serializer.data)

    except Exception as e:
        print(e)
        return Response(
            {
                "success": False,
                "message": "Something went wrong while fetching product",
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
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def update_product(request, product_id):
    try:
        product = Product.objects.prefetch_related('variants').get(id=product_id)
        serializer = ProductCreateSerializer(
            product,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            {"message": "Product updated successfully"},
            status=status.HTTP_200_OK
        )

    except Product.DoesNotExist:
        return Response(
            {"message": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response(
            {
                "message": "Something went wrong while updating product",
                "details": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


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


@api_view(['GET'])
def category_hsn_commission(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Commission (one per category)
    commission_data = None
    if category.commission:
        commission_data = {
            "type": category.commission.commission_type,
            "value": str(category.commission.commission_value)
        }

    # HSN (only ONE per category)
    hsn = HSN.objects.filter(category=category).first()

    hsn_data = None
    if hsn:
        hsn_data = {
            "id": hsn.id,
            "hsn_code": hsn.code,
            "category": category.name
        }

    response_data = {
        "category_id": category.id,
        "category_name": category.name,
        "commission": commission_data,
        "hsn": hsn_data
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
def product_dropdown_list(request):
    """
    GET /api/products/dropdown/

    Response:
    [
      {
        "id": 1,
        "name": "Brand - Product",
        "is_warranty_item": true,
        "is_variants": true/false
      }
    ]

    Latest first
    """
    try:
        products = (
            Product.objects
            .select_related("brand")
            .annotate(
                is_variants=Exists(
                    ProductVariant.objects.filter(product_id=OuterRef("id"))
                )
            )
            .order_by("-id")  # latest first
        )

        data = []
        for p in products:
            brand_name = p.brand.name if p.brand else ""
            product_name = p.name or ""
            subcategory_name = p.subcategory.name if p.subcategory else ""

            # Brand - Product - Subcategory
            if brand_name and product_name:
                full_name = f"{brand_name} - {product_name}"
            else:
                full_name = f"{brand_name} - {subcategory_name} - {p.category.name if p.category else ''}"

            data.append({
                "id": p.id,
                "name": full_name,
                "is_warranty_item": p.is_warranty_item,
                "is_variants": bool(p.is_variants),   # ✅ only boolean
            })

        return Response(
            {"success": True, "count": len(data), "data": data},
            status=status.HTTP_200_OK
        )

    except DatabaseError as db_err:
        return Response(
            {"success": False, "message": "Database error", "error": str(db_err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:
        return Response(
            {"success": False, "message": "Something went wrong", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def product_variants_dropdown(request, product_id):
    """
    GET /api/products/<product_id>/variants/
    Returns:
    [
        { "id": 10, "subbrand":1, "subbrand_name":"abc", "model":2, "model_name":"xyz", ... }
    ]
    But tumko sirf:
        { "id": 10, "name": "Subbrand - Model" }
    chahiye
    """
    try:
        # Product exists check
        if not Product.objects.filter(id=product_id).exists():
            return Response(
                {"success": False, "message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        variants = (
            ProductVariant.objects
            .select_related("subbrand", "model")
            .filter(product_id=product_id)
            .order_by("-id")   # latest first
        )

        data = []
        for v in variants:
            subbrand_name = v.subbrand.name if v.subbrand else ""
            model_name = v.model.name if v.model else ""

            if subbrand_name and model_name:
                full_name = f"{subbrand_name} - {model_name}"
            else:
                full_name = subbrand_name or model_name

            data.append({
                "id": v.id,
                "name": full_name
            })

        return Response(
            {"success": True, "count": len(data), "data": data},
            status=status.HTTP_200_OK
        )

    except DatabaseError as db_err:
        return Response(
            {"success": False, "message": "Database error", "error": str(db_err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:
        return Response(
            {"success": False, "message": "Something went wrong", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )