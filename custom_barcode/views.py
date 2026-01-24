# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from vendor.models import PurchaseItem
from product.models import Product
from .serializers import ProductBarcodeSerializer, VariantBarcodeSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def products_by_category(request, category_id):
    try:
        data = []

        products = Product.objects.filter(
            category_id=category_id,
            status='active'
        ).prefetch_related('variants')

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
        product = Product.objects.get(id=product_id)
        purchase_items = (
            PurchaseItem.objects
            .filter(product=product)
            .order_by('-id')
        )
        print(purchase_items)
        data = []

        for item in purchase_items:
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


        return Response({
            "status": True,
            "product": {
                "id": product.id,
                "name": product.name
            },
            "count": len(data),
            "data": data
        }, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({
            "status": False,
            "message": "Product not found"
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

        return Response({
            "status": True,
            "data": {
                "barcode": purchase_item.barcode,
                "product_name": purchase_item.product.name,
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
