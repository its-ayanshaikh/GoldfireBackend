# serializers.py
from rest_framework import serializers
from product.models import Product

class ProductBarcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'selling_price']