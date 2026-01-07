from django.contrib import admin
from django.utils.html import format_html
from .models import Vendor, Purchase, PurchaseReceipt, VendorReturnMonthly
import os
import calendar
# ----------------------------
# Inline for Receipts in Purchase Page
# ----------------------------
class PurchaseReceiptInline(admin.TabularInline):
    model = PurchaseReceipt
    extra = 0
    readonly_fields = ('uploaded_at', 'preview')
    fields = ('file', 'preview', 'uploaded_at')

    def preview(self, obj):
        """Show thumbnail preview if image file."""
        if obj.file and obj.file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            return format_html(f'<img src="{obj.file.url}" style="max-height: 80px; border-radius:6px;">')
        elif obj.file:
            return format_html(f'<a href="{obj.file.url}" target="_blank">View File</a>')
        return "-"
    preview.short_description = "Preview"


# ----------------------------
# Inline for Purchases in Vendor Page
# ----------------------------
class PurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('purchase_date', 'total', 'notes', 'created_at')
    ordering = ('-purchase_date',)
    show_change_link = True


# ----------------------------
# Vendor Admin
# ----------------------------
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'contact_person', 'phone_number',
        'email', 'gst', 'get_status_color', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'contact_person', 'phone_number', 'email', 'gst')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 50
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Vendor Information', {
            'fields': ('name', 'contact_person', 'phone_number', 'email', 'gst')
        }),
        ('Additional Details', {
            'fields': ('address', 'status')
        }),
        ('System Info', {
            'fields': ('created_at',),
        }),
    )

    inlines = [PurchaseInline]

    # Actions
    actions = ['mark_as_active', 'mark_as_inactive']

    @admin.action(description="Mark selected vendors as Active")
    def mark_as_active(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f"{updated} vendor(s) marked as Active.")

    @admin.action(description="Mark selected vendors as Inactive")
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(status='inactive')
        self.message_user(request, f"{updated} vendor(s) marked as Inactive.")

    def get_status_color(self, obj):
        color = 'green' if obj.status == 'active' else 'red'
        return format_html(f'<b><span style="color:{color}">{obj.status.title()}</span></b>')
    get_status_color.short_description = 'Status'


# ----------------------------
# Purchase Admin
# ----------------------------
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'purchase_date', 'total', 'notes', 'created_at', 'receipt_count')
    list_filter = ('vendor', 'purchase_date', 'created_at')
    search_fields = ('vendor__name', 'notes')
    readonly_fields = ('created_at',)
    ordering = ('-purchase_date',)
    date_hierarchy = 'purchase_date'
    list_per_page = 50

    fieldsets = (
        ('Purchase Information', {
            'fields': ('vendor', 'purchase_date', 'total', 'notes')
        }),
        ('System Info', {
            'fields': ('created_at',),
        }),
    )

    # Inline receipts within Purchase detail page
    inlines = [PurchaseReceiptInline]

    def receipt_count(self, obj):
        count = obj.receipts.count()
        return format_html(f"<b>{count}</b>")
    receipt_count.short_description = "Receipts"


# ----------------------------
# PurchaseReceipt Admin (optional standalone view)
# ----------------------------
@admin.register(PurchaseReceipt)
class PurchaseReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase', 'file_link', 'uploaded_at')
    readonly_fields = ('uploaded_at', 'preview')
    search_fields = ('purchase__vendor__name',)
    ordering = ('-uploaded_at',)
    list_per_page = 50

    def file_link(self, obj):
        if obj.file:
            return format_html(f'<a href="{obj.file.url}" target="_blank">{os.path.basename(obj.file.name)}</a>')
        return "-"
    file_link.short_description = "File"

    def preview(self, obj):
        if obj.file and obj.file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            return format_html(f'<img src="{obj.file.url}" style="max-height: 120px;">')
        return "-"
    preview.short_description = "Preview"

@admin.register(VendorReturnMonthly)
class VendorReturnMonthlyAdmin(admin.ModelAdmin):

    # =========================
    # 📋 LIST VIEW
    # =========================
    list_display = (
        'product_name',
        'vendor_name',
        'branch_name',
        'month_name',
        'year',
        'total_qty',
        'last_updated',
    )

    list_display_links = ('product_name',)

    # =========================
    # 🔍 SEARCH
    # =========================
    search_fields = (
        'product__name',
        'product__model__name',
        'vendor__name',
    )

    # =========================
    # 🎛 FILTERS (Right sidebar)
    # =========================
    list_filter = (
        'year',
        'month',
        'branch',
        'vendor',
        'product__category',
    )

    # =========================
    # 📑 ORDERING
    # =========================
    ordering = ('-year', '-month', 'product__name')

    # =========================
    # 🔒 READ ONLY (Safe Admin)
    # =========================
    readonly_fields = (
        'product',
        'vendor',
        'branch',
        'year',
        'month',
        'total_qty',
        'last_updated',
    )

    # =========================
    # ⚡ PERFORMANCE
    # =========================
    list_select_related = (
        'product',
        'vendor',
        'branch',
        'product__category',
        'product__model',
    )

    # =========================
    # ❌ Disable Add / Delete
    # =========================
    def has_add_permission(self, request):
        return False   # auto generated only

    def has_delete_permission(self, request, obj=None):
        return False   # data integrity

    # =========================
    # 🧠 CUSTOM DISPLAY METHODS
    # =========================
    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = "Product"

    def vendor_name(self, obj):
        return obj.vendor.name
    vendor_name.short_description = "Vendor"

    def branch_name(self, obj):
        return obj.branch.name
    branch_name.short_description = "Branch"

    def month_name(self, obj):
        return calendar.month_name[obj.month]
    month_name.short_description = "Month"
