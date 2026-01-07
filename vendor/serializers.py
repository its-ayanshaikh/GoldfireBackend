from rest_framework import serializers
from .models import Vendor, Purchase, PurchaseReceipt, VendorReturnMonthly


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name", "contact_person", "phone_number", "email", "gst", "status"]


class PurchaseReceiptSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseReceipt
        fields = ["id", "file_url", "uploaded_at"]

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class PurchaseSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    receipts = PurchaseReceiptSerializer(many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = [
            "id",
            "vendor",
            "total",
            "purchase_date",
            "notes",
            "receipts",
            "created_at",
        ]


class VendorReturnMonthlyListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    category = serializers.CharField(source='product.category.name', allow_null=True)
    brand = serializers.CharField(source='product.brand.name', allow_null=True)
    model = serializers.CharField(source='product.model.name', allow_null=True)
    vendor_name = serializers.CharField(source='vendor.name')
    branch_name = serializers.CharField(source='branch.name')

    class Meta:
        model = VendorReturnMonthly
        fields = [
            'id',
            'product_name',
            'category',
            'brand',
            'model',
            'vendor_name',
            'branch_name',
            'month',
            'year',
            'total_qty',
            'last_updated',
        ]
