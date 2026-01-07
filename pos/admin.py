from django.contrib import admin
from .models import (
    Customer, Bill, BillItem, Payment,
    ReturnBill, ReturnItem,
    ReplacementBill, ReplacementItem,
    ReplacementPayment, ReplacementRefund,
    ProductTransfer
)

# -------------------------------------------------
# CUSTOMER
# -------------------------------------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'due_amount', 'created_at')
    search_fields = ('name', 'phone')
    readonly_fields = ('created_at',)


# -------------------------------------------------
# BILL ITEM INLINE
# -------------------------------------------------
class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 0
    readonly_fields = (
        'product', 'qty', 'price',
        'discount_type', 'discount_value',
        'final_amount', 'taxable_value',
        'cgst_amount', 'sgst_amount', 'igst_amount',
        'total', 'serial_number'
    )
    can_delete = False


# -------------------------------------------------
# PAYMENT INLINE
# -------------------------------------------------
class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('payment_method', 'cash_amount', 'upi_amount', 'total_amount', 'payment_date')
    can_delete = False


# -------------------------------------------------
# BILL
# -------------------------------------------------
@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = (
        'bill_number', 'bill_name', 'customer',
        'final_amount', 'is_gst', 'branch', 'date'
    )
    list_filter = ('branch', 'is_gst', 'date')
    search_fields = ('bill_number', 'bill_name', 'customer__name', 'customer__phone')
    readonly_fields = (
        'bill_number', 'date',
        'total_amount', 'total_discount',
        'total_taxable_value',
        'total_cgst', 'total_sgst', 'total_igst',
        'final_amount'
    )
    inlines = [BillItemInline, PaymentInline]


# -------------------------------------------------
# RETURN ITEM INLINE
# -------------------------------------------------
class ReturnItemInline(admin.TabularInline):
    model = ReturnItem
    extra = 0
    readonly_fields = ('product', 'qty', 'price', 'total_refund', 'salesperson')
    can_delete = False


# -------------------------------------------------
# RETURN BILL
# -------------------------------------------------
@admin.register(ReturnBill)
class ReturnBillAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'bill', 'customer',
        'total_refund', 'refund_type',
        'return_destination', 'created_at'
    )
    list_filter = ('refund_type', 'return_destination', 'created_at')
    search_fields = ('bill__bill_number', 'customer__name', 'customer__phone')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ReturnItemInline]


# -------------------------------------------------
# REPLACEMENT ITEM INLINE
# -------------------------------------------------
class ReplacementItemInline(admin.TabularInline):
    model = ReplacementItem
    extra = 0
    readonly_fields = (
        'old_bill_item',
        'old_product', 'new_product',
        'qty',
        'old_price', 'new_price',
        'old_serial_number', 'new_serial_number'
    )
    can_delete = False


# -------------------------------------------------
# REPLACEMENT PAYMENT INLINE
# -------------------------------------------------
class ReplacementPaymentInline(admin.TabularInline):
    model = ReplacementPayment
    extra = 0
    readonly_fields = (
        'payment_method', 'cash_amount',
        'upi_amount', 'total_amount', 'created_at'
    )
    can_delete = False


# -------------------------------------------------
# REPLACEMENT REFUND INLINE
# -------------------------------------------------
class ReplacementRefundInline(admin.TabularInline):
    model = ReplacementRefund
    extra = 0
    readonly_fields = (
        'refund_method', 'cash_amount',
        'upi_amount', 'total_refund', 'created_at'
    )
    can_delete = False


# -------------------------------------------------
# REPLACEMENT BILL
# -------------------------------------------------
@admin.register(ReplacementBill)
class ReplacementBillAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'bill', 'customer',
        'replacement_type', 'difference_amount',
        'return_destination', 'created_at'
    )
    list_filter = ('replacement_type', 'return_destination', 'created_at')
    search_fields = ('bill__bill_number', 'customer__name', 'customer__phone')
    readonly_fields = (
        'old_total_amount',
        'new_total_amount',
        'difference_amount',
        'created_at'
    )
    inlines = [
        ReplacementItemInline,
        ReplacementPaymentInline,
        ReplacementRefundInline
    ]


# -------------------------------------------------
# PRODUCT TRANSFER
# -------------------------------------------------
@admin.register(ProductTransfer)
class ProductTransferAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'from_branch', 'to_branch',
        'quantity', 'status', 'created_at'
    )
    list_filter = ('status', 'from_branch', 'to_branch')
    search_fields = ('product__name',)
    readonly_fields = ('created_at', 'updated_at')
