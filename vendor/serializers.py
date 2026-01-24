from rest_framework import serializers

from product.utils import generate_barcode_text
from .models import Vendor, Purchase, PurchaseReceipt, VendorReturnMonthly, PurchaseItem
from product.serializers import SerialNumberSerializer
from product.models import Stock, SerialNumber

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name", "contact_person", "phone_number", "email", "gst", "status"]


class PurchaseReceiptSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseReceipt
        fields = ['id', 'file', 'uploaded_at']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class PurchaseItemSerializer(serializers.ModelSerializer):
    serials = SerialNumberSerializer(many=True, required=False)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    barcode = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseItem
        fields = [
            'id',
            'product',
            'variant',
            'qty',
            'purchase_price',
            'selling_price',
            'total',
            'barcode',
            'serials'
        ]

    def get_barcode(self, obj):
        branch = self.context.get('branch')
        stock = Stock.objects.filter(
            product=obj.product,
            variant=obj.variant,
            branch=branch
        ).first()
        return stock.barcode if stock else None



class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)
    receipts = PurchaseReceiptSerializer(many=True, required=False)

    class Meta:
        model = Purchase
        fields = [
            'id',
            'vendor',
            'bill_no',
            'purchase_date',
            'total',
            'notes',
            'items',
            'receipts'
        ]

    # ================================
    # CREATE
    # ================================
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        receipts_data = validated_data.pop('receipts', [])
        branch = self.context['branch']

        purchase = Purchase.objects.create(**validated_data)

        self._handle_items(
            purchase=purchase,
            items_data=items_data,
            branch=branch,
            is_update=False
        )

        self._handle_receipts(purchase, receipts_data)

        return purchase

    # ================================
    # UPDATE
    # ================================
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        receipts_data = validated_data.pop('receipts', [])
        branch = self.context['branch']

        # update purchase fields
        for field in ['vendor', 'bill_no', 'purchase_date', 'total', 'notes']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()

        self._handle_items(
            purchase=instance,
            items_data=items_data,
            branch=branch,
            is_update=True
        )

        self._handle_receipts(instance, receipts_data)

        return instance

    # ================================
    # ITEMS HANDLER (CREATE + UPDATE)
    # ================================
    def _handle_items(self, purchase, items_data, branch, is_update):
        existing_items = {
            (item.product_id, item.variant_id): item
            for item in purchase.items.all()
        }

        processed_keys = set()

        for item_data in items_data:
            serials_data = item_data.pop('serials', [])
            key = (item_data['product'].id, item_data['variant'].id)
            processed_keys.add(key)

            # 🔹 SELLING PRICE COPY (frontend se nahi)
            item_data['selling_price'] = (
                item_data['variant'].selling_price
                if item_data.get('variant')
                else item_data['product'].selling_price
            )

            # =====================
            # UPDATE ITEM
            # =====================
            if key in existing_items:
                item = existing_items[key]
                old_qty = item.qty

                for field, value in item_data.items():
                    setattr(item, field, value)
                item.save()

                qty_diff = item.qty - old_qty
                self._update_stock(item, branch, qty_diff)
                self._sync_serials(item, serials_data)

            # =====================
            # CREATE ITEM
            # =====================
            else:
                item = PurchaseItem.objects.create(
                    purchase=purchase,
                    **item_data
                )
                self._update_stock(item, branch, item.qty)
                self._sync_serials(item, serials_data)

        # =====================
        # REMOVE DELETED ITEMS
        # =====================
        if is_update:
            for key, item in existing_items.items():
                if key not in processed_keys:
                    self._update_stock(item, branch, -item.qty)
                    item.delete()

    # ================================
    # STOCK UPDATE
    # ================================
    def _update_stock(self, item, branch, qty_diff):
        stock, _ = Stock.objects.get_or_create(
            product=item.product,
            variant=item.variant,
            branch=branch,
            defaults={'qty': 0}
        )
        
        if not stock.barcode:
            counter = Stock.objects.count() + 1
            category = item.product.category if item.product else None
            stock.barcode = generate_barcode_text(category, counter)

        stock.qty += qty_diff
        stock.save()

    # ================================
    # SERIAL SYNC
    # ================================
    def _sync_serials(self, item, serials_data):
        incoming = set(s['serial_number'] for s in serials_data)
        existing = set(item.serials.values_list('serial_number', flat=True))

        # delete removed
        item.serials.exclude(serial_number__in=incoming).delete()

        # add new
        for serial in incoming - existing:
            SerialNumber.objects.create(
                purchase_item=item,
                product=item.product,
                variant=item.variant,
                serial_number=serial
            )

    # ================================
    # RECEIPTS
    # ================================
    def _handle_receipts(self, purchase, receipts_data):
        for receipt in receipts_data:
            PurchaseReceipt.objects.create(
                purchase=purchase,
                **receipt
            )
            
    def to_representation(self, instance):
        data = super().to_representation(instance)

        # pass branch context to nested serializer
        for item in data.get('items', []):
            item_serializer = PurchaseItemSerializer(
                instance.items.get(id=item['id']),
                context={'branch': self.context['branch']}
            )
            item.update(item_serializer.data)

        return data




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
