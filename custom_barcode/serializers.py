# serializers.py
from rest_framework import serializers
from product.models import Product, ProductVariant

class ProductBarcodeSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'selling_price', 'type']

    def get_type(self, obj):
        return "product"


class VariantBarcodeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'selling_price', 'type']

    def get_name(self, obj):
        return f"{obj.product.name} - {obj.subbrand} - {obj.model}"

    def get_type(self, obj):
        return "variant"
