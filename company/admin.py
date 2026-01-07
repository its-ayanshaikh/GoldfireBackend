from django.contrib import admin
from .models import Company, Branch

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'phone', 'email', 'status', 'created_at')
    list_filter = ('status', 'company')
    search_fields = ('name', 'phone', 'email', 'company__name')
    readonly_fields = ('created_at',)
    ordering = ('company', 'name')
