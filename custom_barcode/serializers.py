# serializers.py
from rest_framework import serializers
from product.models import Product, ProductVariant
from product.utils import build_display_name


class ProductBarcodeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'selling_price', 'type']

    def get_name(self, obj):
        # Never blank (covers etc.)
        return build_display_name(obj)

    def get_type(self, obj):
        return "product"


class VariantBarcodeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'selling_price', 'type']

    def get_name(self, obj):
        # Base display name (never blank), then append sub-brand / model
        # details when they are not already part of the name.
        name = build_display_name(obj.product, obj)
        extras = []
        subbrand = obj.subbrand.name if obj.subbrand else ""
        model = obj.model.name if obj.model else ""
        if subbrand and subbrand not in name:
            extras.append(subbrand)
        if model and model not in name:
            extras.append(model)
        return " - ".join([name] + extras) if extras else name

    def get_type(self, obj):
        return "variant"
