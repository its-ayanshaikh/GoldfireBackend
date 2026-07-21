from rest_framework import serializers
from product.models import Product
# from product.serializers import QuantitySerializer
from rest_framework import serializers
from .models import Bill, BillItem, Payment, Customer, Expense
from employee.models import Employee
from django.db.models import Sum
from product.utils import build_display_name


class ExpenseSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Expense
        fields = [
            'id', 'branch', 'branch_name', 'name', 'amount',
            'payment_method', 'notes', 'created_by', 'created_by_name',
            'date', 'created_at',
        ]
        read_only_fields = ['id', 'branch', 'branch_name', 'created_by', 'created_by_name', 'created_at']


# class RackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rack
#         fields = ['id', 'name', 'branch']
#         read_only_fields = ['branch']  # branch auto set hogi backend se


class ProductBranchSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    quantities = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category_name', 'brand_name',
            'selling_price', 'min_selling_price',
            'commission_type', 'commission_value',
            'is_warranty_item', 'warranty_period',
            'quantities',
        ]

    def get_quantities(self, obj):
        branch = self.context.get('branch')
        queryset = obj.quantities.filter(branch=branch)
        # return QuantitySerializer(queryset, many=True).data


# --------------------------
# CUSTOMER SERIALIZER
# --------------------------
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'due_amount']


# --------------------------
# SALESPERSON SERIALIZER (MINI)
# --------------------------
class SalespersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name']


# --------------------------
# PRODUCT SERIALIZER (MINI)
# --------------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'selling_price', 'commission_type', 'commission_value']


# --------------------------
# BILL ITEM SERIALIZER
# --------------------------    
class BillItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    salesperson = SalespersonSerializer(read_only=True)
    model_name = serializers.SerializerMethodField()
    returned_qty = serializers.SerializerMethodField()

    class Meta:
        model = BillItem
        fields = [
            'id', 'product', 'salesperson', 'model_name',
            'qty', 'price', 'discount_type',
            'discount_value', 'final_amount', 'total',
            'is_returned', 'returned_qty', 'serial_number'
        ]

    def get_model_name(self, obj):
        # model variant pe hota hai, product pe nahi
        if obj.variant and obj.variant.model:
            return obj.variant.model.name
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Never show a blank product name (e.g. covers stored without a name):
        # fall back to "<category> - <model>". Uses the line's own variant.
        if isinstance(data.get('product'), dict):
            data['product']['name'] = build_display_name(instance.product, instance.variant)
        return data

    def get_returned_qty(self, obj):
        # is bill item ke against kitni qty already return ho chuki
        agg = obj.returnitem_set.aggregate(total=Sum('qty')) if hasattr(obj, 'returnitem_set') else None
        if agg and agg.get('total'):
            return agg['total']
        # fallback via related name
        from .models import ReturnItem
        total = ReturnItem.objects.filter(original_bill_item=obj).aggregate(total=Sum('qty'))['total']
        return total or 0


# --------------------------
# PAYMENT SERIALIZER
# --------------------------
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_method', 'cash_amount', 'upi_amount', 'total_amount', 'payment_date']


# --------------------------
# BILL SERIALIZER (MAIN)
# --------------------------
class BillListSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    items = BillItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = Bill
        fields = [
            'id', 'bill_number', 'customer', 'branch_name',
            'date', 'total_amount', 'total_discount', 'final_amount',
            'items', 'payments'
        ]
