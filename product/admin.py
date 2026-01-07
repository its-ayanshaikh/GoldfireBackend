from django.contrib import admin
from .models import (
    Category, SubCategory, Brand, SubBrand, Model,
    Type, HSN, Product, Quantity, SerialNumber, Rack
)

@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch')
    list_filter = ('branch',)
    search_fields = ('name', 'branch__name')
    autocomplete_fields = ('branch',)

# ---------- INLINE (Quantity inside Product) ----------
class QuantityInline(admin.TabularInline):
    model = Quantity
    extra = 1
    autocomplete_fields = ('branch', 'rack')  # ✅ add rack
    readonly_fields = ('updated_at',)
    fields = ('branch', 'rack', 'qty', 'barcode', 'updated_at')  # ✅ rack added


# ---------- INLINE (Serial Numbers inside Product) ----------
class SerialNumberInline(admin.TabularInline):
    model = SerialNumber
    extra = 1
    readonly_fields = ('purchase_date',)
    fields = ('serial_number', 'is_available', 'purchase_date')
    show_change_link = True


# ---------- CATEGORY ----------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# ---------- SUBCATEGORY ----------
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    autocomplete_fields = ('category',)


# ---------- BRAND ----------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    autocomplete_fields = ('category',)


# ---------- SUBBRAND ----------
@admin.register(SubBrand)
class SubBrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'subcategory')
    list_filter = ('category', 'subcategory')
    search_fields = ('name', 'category__name', 'subcategory__name')
    autocomplete_fields = ('category', 'subcategory')


# ---------- MODEL ----------
@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subbrand')
    list_filter = ('subbrand', 'subbrand__category')
    search_fields = ('name', 'subbrand__name', 'subbrand__category__name')
    autocomplete_fields = ('subbrand',)


# ---------- TYPE ----------
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    autocomplete_fields = ('category',)


# ---------- HSN ----------
@admin.register(HSN)
class HSNAdmin(admin.ModelAdmin):
    list_display = ('code', 'category', 'cgst', 'sgst', 'igst')
    list_filter = ('category',)
    search_fields = ('code', 'category__name')
    autocomplete_fields = ('category',)


# ---------- PRODUCT ----------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'category', 'subcategory', 'brand', 'subbrand',
        'model', 'type', 'vendor', 'selling_price', 'min_selling_price',
        'status', 'is_warranty_item', 'warranty_period', 'created_at'
    )
    list_filter = (
        'category', 'subcategory', 'brand', 'subbrand',
        'type', 'status', 'vendor', 'is_warranty_item'
    )
    search_fields = (
        'name', 'brand__name', 'subbrand__name',
        'category__name', 'subcategory__name', 'vendor__name', 'type__name'
    )
    readonly_fields = ('created_at',)
    autocomplete_fields = (
        'category', 'subcategory', 'brand', 'subbrand',
        'model', 'type', 'vendor', 'hsn'
    )

    # ✅ Show both quantity and serial number inline
    inlines = [QuantityInline, SerialNumberInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'status', 'created_at')
        }),
        ('Relations', {
            'fields': (
                'category', 'subcategory', 'brand', 'subbrand',
                'model', 'type', 'vendor', 'hsn'
            )
        }),
        ('Pricing & Commission', {
            'fields': (
                'purchase_price', 'selling_price', 'min_selling_price',
                'commission_type', 'commission_value'
            )
        }),
        ('Warranty Info', {
            'fields': ('is_warranty_item', 'warranty_period')
        }),
        ('Stock Settings', {
            'fields': ('min_qty_alert',)
        }),
    )


# ---------- QUANTITY ----------
@admin.register(Quantity)
class QuantityAdmin(admin.ModelAdmin):
    list_display = ('product', 'branch', 'rack', 'qty', 'barcode', 'updated_at')  # ✅ rack added
    list_filter = ('branch', 'rack', 'product__category', 'product__brand')  # ✅ rack filter added
    search_fields = ('product__name', 'branch__name', 'rack__name')  # ✅ rack search added
    autocomplete_fields = ('product', 'branch', 'rack')  # ✅ rack autocomplete



# ---------- SERIAL NUMBER ----------
@admin.register(SerialNumber)
class SerialNumberAdmin(admin.ModelAdmin):
    list_display = ('product', 'serial_number', 'is_available', 'purchase_date')
    list_filter = ('is_available', 'product__category', 'product__brand')
    search_fields = ('serial_number', 'product__name')
    autocomplete_fields = ('product',)
