from rest_framework import serializers
from .models import Brand, Category, SubCategory, Model, SubBrand, Type, HSN, Product, Quantity, Commission, SerialNumber

class CommissionSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    assigned_categories = serializers.SerializerMethodField()

    class Meta:
        model = Commission
        fields = [
            'id',
            'name',
            'commission_type',
            'commission_value',
            'categories',
            'assigned_categories',
        ]

    def get_assigned_categories(self, obj):
        return list(obj.categories.values("id", "name"))

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        

class HSNSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = HSN
        fields = [
            'id', 'code', 'cgst', 'sgst', 'igst',
            'category', 'category_name', 'description'
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category', 'category_name']
        

class BrandSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Brand
        fields = ['id', 'name', 'image', 'category', 'category_name']


class ModelSerializer(serializers.ModelSerializer):
    subbrand_name = serializers.CharField(source='subbrand.name', read_only=True)
    category_name = serializers.CharField(source='subbrand.category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subbrand.subcategory.name', read_only=True)

    class Meta:
        model = Model
        fields = ['id', 'name', 'subbrand', 'subbrand_name', 'category_name', 'subcategory_name']


class SubBrandSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)

    class Meta:
        model = SubBrand
        fields = ['id', 'name', 'category', 'category_name', 'image', 'subcategory', 'subcategory_name']
        

class TypeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Type
        fields = ['id', 'name', 'category', 'category_name']


# ---------- QUANTITY SERIALIZER ----------
class QuantitySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    rack_name = serializers.CharField(source='rack.name', read_only=True)

    class Meta:
        model = Quantity
        fields = [
            'id', 'product', 'product_name',
            'branch', 'branch_name',
            'qty', 'barcode', 'rack', 'rack_name', 'updated_at'
        ]

class SerialNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerialNumber
        fields = [
            'id',
            'serial_number',
            'is_available',
            'purchase_date',
        ]


# ---------- PRODUCT SERIALIZER ----------
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    subbrand_name = serializers.CharField(source='subbrand.name', read_only=True)
    model_name = serializers.CharField(source='model.name', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    hsn_code = serializers.CharField(source='hsn.code', read_only=True)

    quantities = QuantitySerializer(many=True, read_only=True)
    serial_numbers = serializers.SerializerMethodField()   

    class Meta:
        model = Product
        fields = [
            'id', 'name',
            'category', 'category_name',
            'subcategory', 'subcategory_name',
            'brand', 'brand_name',
            'subbrand', 'subbrand_name',
            'model', 'model_name',
            'type', 'type_name',
            'vendor', 'vendor_name',
            'hsn', 'hsn_code',
            'purchase_price', 'selling_price', 'min_selling_price',
            'min_qty_alert', 'commission_type', 'commission_value',
            'status', 'created_at',
            'is_warranty_item', 'warranty_period',   # ✅ new fields added
            'quantities','serial_numbers',
        ]
        
    def get_serial_numbers(self, obj):
        """
        Serial numbers sirf warranty items ke liye bhejo
        """
        if not obj.is_warranty_item:
            return None   # ❌ non-warranty -> null

        qs = obj.serial_numbers.all()
        return SerialNumberSerializer(qs, many=True).data