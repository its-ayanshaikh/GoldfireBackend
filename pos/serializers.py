from rest_framework import serializers
from product.models import Product
# from product.serializers import QuantitySerializer
from rest_framework import serializers
from .models import Bill, BillItem, Payment, Customer
from employee.models import Employee


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
    model_name = serializers.CharField(source='model.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'selling_price', 'commission_type', 'commission_value', 'model_name']


# --------------------------
# BILL ITEM SERIALIZER
# --------------------------    
class BillItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    salesperson = SalespersonSerializer(read_only=True)

    class Meta:
        model = BillItem
        fields = [
            'id', 'product', 'salesperson',
            'qty', 'price', 'discount_type',
            'discount_value', 'final_amount', 'total', 'is_returned', 'serial_number'
        ]


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
