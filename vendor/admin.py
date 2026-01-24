from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Vendor,
    Purchase,
    PurchaseItem,
    PurchaseReceipt,
    VendorReturnMonthly
)
import calendar


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0
    autocomplete_fields = ('product', 'variant')
    fields = (
        'product',
        'barcode',
        'variant',
        'qty',
        'purchase_price',
        'selling_price',
        'total',
    )
    
    
class PurchaseReceiptInline(admin.TabularInline):
    model = PurchaseReceipt
    extra = 0
    readonly_fields = ('uploaded_at', 'preview')
    fields = ('file', 'preview', 'uploaded_at')

    def preview(self, obj):
        if obj.file and obj.file.name.lower().endswith(('.jpg','.jpeg','.png','.webp')):
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:6px;" />',
                obj.file.url
            )
        elif obj.file:
            return format_html('<a href="{}" target="_blank">View</a>', obj.file.url)
        return "-"

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'contact_person', 'phone_number',
        'email', 'gst', 'status', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'contact_person', 'phone_number', 'email', 'gst')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 50


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'vendor',
        'bill_no',
        'purchase_date',
        'total',
        'created_at',
        'item_count',
        'receipt_count'
    )

    list_filter = ('vendor', 'purchase_date')
    search_fields = ('vendor__name', 'bill_no', 'notes')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Purchase Info', {
            'fields': ('vendor', 'bill_no', 'purchase_date', 'total', 'notes')
        }),
        ('System', {
            'fields': ('created_at',)
        }),
    )

    inlines = [PurchaseItemInline, PurchaseReceiptInline]
    date_hierarchy = 'purchase_date'
    ordering = ('-purchase_date',)

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Items"

    def receipt_count(self, obj):
        return obj.receipts.count()
    receipt_count.short_description = "Receipts"


@admin.register(PurchaseReceipt)
class PurchaseReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase', 'file_link', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    ordering = ('-uploaded_at',)

    def file_link(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.file.url,
                obj.file.name.split('/')[-1]
            )
        return "-"

@admin.register(VendorReturnMonthly)
class VendorReturnMonthlyAdmin(admin.ModelAdmin):

    list_display = (
        'variant_name',
        'vendor',
        'branch',
        'month_name',
        'year',
        'total_qty',
        'last_updated',
    )

    search_fields = (
        'variant__product__name',
        'variant__model__name',
        'vendor__name',
    )

    list_filter = (
        'year',
        'month',
        'branch',
        'vendor',
        'variant__product__category',
    )

    ordering = ('-year', '-month')

    readonly_fields = (
        'variant',
        'vendor',
        'branch',
        'year',
        'month',
        'total_qty',
        'last_updated',
    )

    list_select_related = (
        'variant',
        'variant__product',
        'variant__model',
        'vendor',
        'branch',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def variant_name(self, obj):
        parts = [obj.variant.product.name]
        if obj.variant.model:
            parts.append(obj.variant.model.name)
        return " - ".join(parts)

    variant_name.short_description = "Product / Model"

    def month_name(self, obj):
        return calendar.month_name[obj.month]
    month_name.short_description = "Month"
