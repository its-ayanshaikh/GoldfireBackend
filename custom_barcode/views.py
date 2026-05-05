# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from vendor.models import PurchaseItem
from product.models import Product, ProductVariant
from employee.pagination import EmployeePagination
from .serializers import ProductBarcodeSerializer, VariantBarcodeSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def products_by_category(request, category_id):
    try:
        data = []

        products = Product.objects.filter(
            category_id=category_id,
            status='active'
        ).prefetch_related('variants').filter(
            status='active'
        )
    
        for product in products:
            variants = product.variants.all()

            # 🔹 Agar variants hain → variants bhejo
            if variants.exists():
                serializer = VariantBarcodeSerializer(variants, many=True)
                data.extend(serializer.data)

            # 🔹 Agar variants nahi hain → product bhejo
            else:
                serializer = ProductBarcodeSerializer(product)
                data.append(serializer.data)

        return Response({
            "status": True,
            "count": len(data),
            "data": data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": False,
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_variant_purchases(request, product_id):
    try:
        variant = None
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            variant = ProductVariant.objects.select_related("product").get(id=product_id)
            product = variant.product

        base_qs = PurchaseItem.objects.select_related(
            "purchase",
            "purchase__vendor",
            "variant",
        )
        if variant:
            purchase_items = base_qs.filter(variant=variant).order_by("-id")
        else:
            purchase_items = base_qs.filter(product=product).order_by("-id")
        search = request.query_params.get("search")
        if search:
            purchase_items = purchase_items.filter(
                Q(product__name__icontains=search) |
                Q(variant__model__name__icontains=search) |
                Q(variant__subbrand__name__icontains=search)
            )

        paginator = EmployeePagination()
        page = paginator.paginate_queryset(purchase_items, request)

        data = []

        for item in page:
            data.append({
                "purchase_item_id": item.id,
                "variant": (
                    {
                        "id": item.variant.id,
                        "name": str(item.variant)
                    } if item.variant else None
                ),
                "selling_price": float(item.selling_price),
                "vendor_name": item.purchase.vendor.name
            })

        return paginator.get_paginated_response({
            "status": True,
            "product": {
                "id": product.id,
                "name": product.name
            },
            "variant": (
                {
                    "id": variant.id,
                    "name": str(variant)
                } if variant else None
            ),
            "results": data
        })

    # except Product.DoesNotExist:
    #     return Response({
    #         "status": False,
    #         "message": "Product not found"
    #     }, status=status.HTTP_404_NOT_FOUND)

    except ProductVariant.DoesNotExist:
        return Response({
            "status": False,
            "message": "Product or variant not found"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "status": False,
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_barcode(request):
    try:
        purchase_item_id = request.query_params.get('purchase_item_id')

        if not purchase_item_id:
            return Response({
                "status": False,
                "message": "purchase_item_id is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        # 🔍 PurchaseItem fetch (barcode yahin se aayega)
        purchase_item = PurchaseItem.objects.select_related(
            'product'
        ).get(id=purchase_item_id)
        
        variant_name = None
        if purchase_item.variant:
            subbrand_name = purchase_item.variant.subbrand.name if purchase_item.variant.subbrand else ""
            model_name = purchase_item.variant.model.name if purchase_item.variant.model else ""

            if subbrand_name and model_name:
                variant_name = f"{subbrand_name} - {model_name}"
            else:
                variant_name = subbrand_name or model_name or str(purchase_item.variant)

        return Response({
            "status": True,
            "data": {
                "barcode": purchase_item.barcode,
                "product_name": purchase_item.product.name,
                "variant_name": variant_name,
                "selling_price": float(purchase_item.selling_price),
            }
        }, status=status.HTTP_200_OK)

    except PurchaseItem.DoesNotExist:
        return Response({
            "status": False,
            "message": "Purchase item not found"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "status": False,
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
