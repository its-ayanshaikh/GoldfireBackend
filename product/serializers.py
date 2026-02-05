from rest_framework import serializers
from .models import Brand, Category, Stock, SubCategory, Model, SubBrand, Type, HSN, Product, Commission, SerialNumber, ProductVariant
from django.db.models import Sum

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

    class Meta:
        model = Model
        fields = ['id', 'name', 'subbrand', 'subbrand_name']


class SubBrandSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(
        source='subcategory.name',
        read_only=True
    )

    class Meta:
        model = SubBrand
        fields = [
            'id',
            'name',
            'subcategory',        # 👈 create/update ke liye
            'subcategory_name'    # 👈 response ke liye
        ]

        

class TypeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Type
        fields = ['id', 'name', 'category', 'category_name']


# # ---------- QUANTITY SERIALIZER ----------
# class QuantitySerializer(serializers.ModelSerializer):
#     product_name = serializers.CharField(source='product.name', read_only=True)
#     branch_name = serializers.CharField(source='branch.name', read_only=True)
#     rack_name = serializers.CharField(source='rack.name', read_only=True)

#     class Meta:
#         model = Quantity
#         fields = [
#             'id', 'product', 'product_name',
#             'branch', 'branch_name',
#             'qty', 'barcode', 'rack', 'rack_name', 'updated_at'
#         ]

class SerialNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerialNumber
        fields = ['id', 'serial_number', 'is_available']



class ProductVariantGroupSerializer(serializers.Serializer):
    subbrand = serializers.IntegerField()
    model = serializers.ListField(
        child=serializers.IntegerField()
    )
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    minimum_selling_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    minimum_quantity = serializers.IntegerField()



# ---------- PRODUCT SERIALIZER ----------
class ProductCreateSerializer(serializers.ModelSerializer):
    variants = ProductVariantGroupSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'subcategory',
            'hsn',
            'type',
            'brand',
            'selling_price',
            'minimum_selling_price',
            'minimum_quantity',
            'commission_type',
            'commission_value',
            'status',
            'is_warranty_item',
            'warranty_period',
            'variants'
        ]

    def create(self, validated_data):
        variants_data = validated_data.pop('variants', [])
        product = Product.objects.create(**validated_data)

        self._sync_variants(product, variants_data)
        return product

    def update(self, instance, validated_data):
        variants_data = validated_data.pop('variants', None)

        # update product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if variants_data is not None:
            self._sync_variants(instance, variants_data)

        return instance

    def _sync_variants(self, product, variants_data):
        """
        ✔ create new
        ✔ update existing
        ✔ delete removed
        ✔ NO DUPLICATES
        """

        existing = {
            (v.subbrand_id, v.model_id): v
            for v in product.variants.all()
        }

        incoming_keys = set()

        for variant in variants_data:
            subbrand_id = variant['subbrand']

            for model_id in variant['model']:
                key = (subbrand_id, model_id)
                incoming_keys.add(key)

                if key in existing:
                    # 🔁 update existing variant
                    v = existing[key]
                    v.selling_price = variant['selling_price']
                    v.minimum_selling_price = variant['minimum_selling_price']
                    v.minimum_quantity = variant['minimum_quantity']
                    v.save()
                else:
                    # ➕ create new variant
                    ProductVariant.objects.create(
                        product=product,
                        subbrand_id=subbrand_id,
                        model_id=model_id,
                        selling_price=variant['selling_price'],
                        minimum_selling_price=variant['minimum_selling_price'],
                        minimum_quantity=variant['minimum_quantity']
                    )

        # ❌ delete removed variants
        for key, variant_obj in existing.items():
            if key not in incoming_keys:
                variant_obj.delete()


class ProductVariantListSerializer(serializers.ModelSerializer):
    subbrand_name = serializers.CharField(source='subbrand.name', read_only=True)
    model_name = serializers.CharField(source='model.name', read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'subbrand',
            'subbrand_name',
            'model',
            'model_name',
            'selling_price',
            'minimum_selling_price',
            'minimum_quantity'
        ]


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    variants = serializers.SerializerMethodField()
    is_variant = serializers.SerializerMethodField()
    total_qty = serializers.SerializerMethodField()
    branch_qty = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',            
            'category_name',
            'hsn',
            'type',
            'brand',
            'brand_name',
            'selling_price',
            'minimum_selling_price',
            'minimum_quantity',
            'commission_type',
            'commission_value',
            'status',
            'is_variant',
            'variants',
            'is_warranty_item',
            'warranty_period',
            'created_at',
            'total_qty',
            'branch_qty'
        ]
        
    def get_total_qty(self, obj):

        # agar variants hai → variants ka sum
        if obj.variants.exists():
            qty = Stock.objects.filter(
                variant__product=obj
            ).aggregate(total=Sum('qty'))['total']
        else:
            # simple product → product level stock
            qty = Stock.objects.filter(
                product=obj,
                variant__isnull=True
            ).aggregate(total=Sum('qty'))['total']

        return qty or 0


    def get_branch_qty(self, obj):
        if obj.variants.exists():
            qs = Stock.objects.filter(
                variant__product=obj
            ).values(
                'branch_id',
                'branch__name'
            ).annotate(qty=Sum('qty'))
        else:
            qs = Stock.objects.filter(
                product=obj,
                variant__isnull=True
            ).values(
                'branch_id',
                'branch__name'
            ).annotate(qty=Sum('qty'))

        return [
            {
                "branch_id": x['branch_id'],
                "branch_name": x['branch__name'],
                "qty": x['qty']
            }
            for x in qs
        ]


    def get_is_variant(self, obj):
        return obj.variants.exists()

    def get_variants(self, obj):
        data = []

        for v in obj.variants.all():

            total_qty = Stock.objects.filter(
                variant=v
            ).aggregate(total=Sum('qty'))['total'] or 0

            branch_qs = Stock.objects.filter(
                variant=v
            ).values(
                'branch_id',
                'branch__name'
            ).annotate(qty=Sum('qty'))

            subcategory = (
                v.subbrand.subcategory
                if v.subbrand and v.subbrand.subcategory
                else None
            )

            data.append({
                "variant_id": v.id,

                # ✅ IDs
                "subcategory_id": subcategory.id if subcategory else None,
                "subcategory_name": subcategory.name if subcategory else None,

                "subbrand_id": v.subbrand.id if v.subbrand else None,
                "subbrand": v.subbrand.name if v.subbrand else None,

                "model_id": v.model.id if v.model else None,
                "model": v.model.name if v.model else None,

                "selling_price": v.selling_price,
                "minimum_selling_price": v.minimum_selling_price,
                "minimum_quantity": v.minimum_quantity,
                "total_qty": total_qty,

                "branch_qty": [
                    {
                        "branch_id": b['branch_id'],
                        "branch_name": b['branch__name'],
                        "qty": b['qty']
                    }
                    for b in branch_qs
                ]
            })

        return data


class ProductDetailsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    variants = serializers.SerializerMethodField()
    is_variant = serializers.SerializerMethodField()
    total_qty = serializers.SerializerMethodField()
    branch_qty = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',            
            'category_name',
            'hsn',
            'type',
            'brand',
            'brand_name',
            'selling_price',
            'minimum_selling_price',
            'minimum_quantity',
            'commission_type',
            'commission_value',
            'status',
            'is_variant',
            'variants',
            'is_warranty_item',
            'warranty_period',
            'created_at',
            'total_qty',
            'branch_qty'
        ]
        
    def get_total_qty(self, obj):

        # agar variants hai → variants ka sum
        if obj.variants.exists():
            qty = Stock.objects.filter(
                variant__product=obj
            ).aggregate(total=Sum('qty'))['total']
        else:
            # simple product → product level stock
            qty = Stock.objects.filter(
                product=obj,
                variant__isnull=True
            ).aggregate(total=Sum('qty'))['total']

        return qty or 0


    def get_branch_qty(self, obj):
        if obj.variants.exists():
            qs = Stock.objects.filter(
                variant__product=obj
            ).values(
                'branch_id',
                'branch__name'
            ).annotate(qty=Sum('qty'))
        else:
            qs = Stock.objects.filter(
                product=obj,
                variant__isnull=True
            ).values(
                'branch_id',
                'branch__name'
            ).annotate(qty=Sum('qty'))

        return [
            {
                "branch_id": x['branch_id'],
                "branch_name": x['branch__name'],
                "qty": x['qty']
            }
            for x in qs
        ]


    def get_is_variant(self, obj):
        return obj.variants.exists()

    def get_variants(self, obj):
        variants_map = {}

        for v in obj.variants.all():

            # 🔑 grouping key
            key = (
                v.subbrand_id,
                v.selling_price,
                v.minimum_selling_price,
                v.minimum_quantity
            )

            subcategory = (
                v.subbrand.subcategory
                if v.subbrand and v.subbrand.subcategory
                else None
            )

            # total qty per model
            model_qty = Stock.objects.filter(
                variant=v
            ).aggregate(total=Sum('qty'))['total'] or 0

            branch_qs = Stock.objects.filter(
                variant=v
            ).values(
                'branch_id',
                'branch__name'
            ).annotate(qty=Sum('qty'))

            if key not in variants_map:
                variants_map[key] = {
                    "subcategory_id": subcategory.id if subcategory else None,
                    "subcategory_name": subcategory.name if subcategory else None,

                    "subbrand_id": v.subbrand.id if v.subbrand else None,
                    "subbrand": v.subbrand.name if v.subbrand else None,

                    "selling_price": v.selling_price,
                    "minimum_selling_price": v.minimum_selling_price,
                    "minimum_quantity": v.minimum_quantity,

                    "total_qty": 0,
                    "models": [],
                    "branch_qty_map": {}
                }

            # 🔹 add model
            if v.model:
                variants_map[key]["models"].append({
                    "id": v.model.id,
                    "name": v.model.name
                })

            # 🔹 add qty
            variants_map[key]["total_qty"] += model_qty

            # 🔹 merge branch qty
            for b in branch_qs:
                bid = b["branch_id"]
                if bid not in variants_map[key]["branch_qty_map"]:
                    variants_map[key]["branch_qty_map"][bid] = {
                        "branch_id": bid,
                        "branch_name": b["branch__name"],
                        "qty": 0
                    }
                variants_map[key]["branch_qty_map"][bid]["qty"] += b["qty"]

        # 🔥 final clean list
        data = []
        for v in variants_map.values():
            v["branch_qty"] = list(v.pop("branch_qty_map").values())
            data.append(v)

        return data


