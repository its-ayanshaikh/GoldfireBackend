# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from product.models import Product, Quantity
from .serializers import ProductBarcodeSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def products_by_category(request, category_id):
    try:
        products = Product.objects.filter(
            category_id=category_id,
            status='active'
        ).only('id', 'name', 'selling_price')

        serializer = ProductBarcodeSerializer(products, many=True)

        return Response({
            "status": True,
            "count": products.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": False,
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_barcode(request):
    try:
        product_id = request.query_params.get('product_id')
        branch_id = request.query_params.get('branch_id')

        if not product_id or not branch_id:
            return Response({
                "status": False,
                "message": "product_id and branch_id are required"
            }, status=status.HTTP_400_BAD_REQUEST)

        quantity = Quantity.objects.select_related(
            'product', 'branch'
        ).get(
            product_id=product_id,
            branch_id=branch_id
        )
        
        print(quantity.barcode)

        return Response({
            "status": True,
            "data": {
                "barcode": quantity.barcode,
                "product_name": quantity.product.name,
                "selling_price": quantity.product.selling_price,
                "branch_name": quantity.branch.name
            }
        }, status=status.HTTP_200_OK)

    except Quantity.DoesNotExist:
        return Response({
            "status": False,
            "message": "Barcode not found for given product & branch"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "status": False,
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)