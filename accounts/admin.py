from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # ------------------------
    # List view configuration
    # ------------------------
    list_display = (
        'username', 'email', 'role', 'branch', 
        'is_active', 'is_staff', 'colored_role', 'last_login'
    )
    list_filter = ('role', 'branch', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('role', 'branch')

    # ------------------------
    # Readonly fields
    # ------------------------
    readonly_fields = ('last_login', 'date_joined')

    # ------------------------
    # Fieldsets organization
    # ------------------------
    fieldsets = (
        ('Login Info', {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Role & Branch', {
            'fields': ('role', 'branch')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'branch', 'is_active', 'is_staff'),
        }),
    )

    # ------------------------
    # Custom Color Display for Role
    # ------------------------
    def colored_role(self, obj):
        color_map = {
            'admin': 'green',
            'subadmin': 'blue',
            'cashier': 'orange'
        }
        color = color_map.get(obj.role, 'black')
        return format_html(f'<b><span style="color:{color}">{obj.get_role_display()}</span></b>')
    colored_role.short_description = 'Role'

    # ------------------------
    # Custom Admin Actions
    # ------------------------
    actions = ['make_active', 'make_inactive']

    @admin.action(description="✅ Activate selected users")
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} user(s) activated.")

    @admin.action(description="🚫 Deactivate selected users")
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} user(s) deactivated.")
