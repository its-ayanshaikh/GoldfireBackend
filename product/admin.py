from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, SubCategory,
    Brand, SubBrand, Model,
    Type, HSN,
    Product, ProductVariant,
    Stock, SerialNumber
)

# =====================================================
# CATEGORY
# =====================================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# =====================================================
# SUB CATEGORY
# =====================================================
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    autocomplete_fields = ('category',)


# =====================================================
# BRAND
# =====================================================
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'logo')
    list_filter = ('category',)
    search_fields = ('name',)
    autocomplete_fields = ('category',)

    def logo(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:6px;" />',
                obj.image.url
            )
        return "-"
    logo.short_description = "Image"


# =====================================================
# SUB BRAND
# =====================================================
@admin.register(SubBrand)
class SubBrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# =====================================================
# MODEL (PHONE MODEL)
# =====================================================
@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subbrand')
    list_filter = ('subbrand',)
    search_fields = ('name', 'subbrand__name')
    autocomplete_fields = ('subbrand',)


# =====================================================
# TYPE
# =====================================================
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    autocomplete_fields = ('category',)


# =====================================================
# HSN
# =====================================================
@admin.register(HSN)
class HSNAdmin(admin.ModelAdmin):
    list_display = ('code', 'category', 'cgst', 'sgst', 'igst')
    list_filter = ('category',)
    search_fields = ('code',)
    autocomplete_fields = ('category',)


# =====================================================
# INLINE → STOCK (QTY HERE ✅)
# =====================================================
class StockInline(admin.TabularInline):
    model = Stock
    extra = 0
    autocomplete_fields = ('branch',)
    fields = ('branch', 'qty')
    readonly_fields = ()


# =====================================================
# INLINE → VARIANT
# =====================================================
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    autocomplete_fields = ('subbrand', 'model')
    fields = (
        'subbrand',
        'model',
        'selling_price',
    )


# =====================================================
# PRODUCT
# =====================================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'subcategory',
        'brand',
        'status',
        'created_at',
    )

    list_filter = (
        'category',
        'subcategory',
        'brand',
        'status',
        'is_warranty_item',
    )

    search_fields = (
        'name',
        'brand__name',
        'category__name',
        'subcategory__name',
    )

    readonly_fields = ('created_at',)

    autocomplete_fields = (
        'category',
        'subcategory',
        'brand',
    )

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'status', 'created_at')
        }),
        ('Classification', {
            'fields': ('category', 'subcategory', 'brand', 'type')
        }),
        ('Commission', {
            'fields': ('commission_type', 'commission_value', 'hsn')
        }),
        ('Warranty', {
            'fields': ('is_warranty_item', 'warranty_period')
        }),
    )

    inlines = [ProductVariantInline]


# =====================================================
# PRODUCT VARIANT (MODEL-WISE ITEM)
# =====================================================
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'variant_name',
        'selling_price',
    )

    search_fields = (
        'product__name',
        'model__name',
    )

    autocomplete_fields = ('product', 'subbrand', 'model')

    inlines = [StockInline]

    def variant_name(self, obj):
        parts = [obj.product.name]
        if obj.model:
            parts.append(obj.model.name)
        return " - ".join(parts)
    variant_name.short_description = "Variant"


# =====================================================
# STOCK (BRANCH-WISE QTY)
# =====================================================
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'variant_name',
        'branch',
        'qty',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'variant',
            'variant__product',
            'variant__model',
            'product',
            'branch'
        )

    def variant_name(self, obj):
        if not obj.variant:
            return obj.product.name if obj.product else "-"

        parts = []
        if obj.variant.product:
            parts.append(obj.variant.product.name)
        if obj.variant.model:
            parts.append(obj.variant.model.name)

        return " - ".join(parts)
    
    variant_name.short_description = "Product / Model"


# =====================================================
# SERIAL NUMBER
# =====================================================
@admin.register(SerialNumber)
class SerialNumberAdmin(admin.ModelAdmin):
    list_display = (
        'variant_name',
        'serial_number',
        'is_available',
    )

    autocomplete_fields = ('variant',)

    def variant_name(self, obj):
        if not obj.variant:
            return obj.product.name if obj.product else "-"

        parts = []
        if obj.variant.product:
            parts.append(obj.variant.product.name)
        if obj.variant.model:
            parts.append(obj.variant.model.name)

        return " - ".join(parts)
    variant_name.short_description = "Product / Model"
