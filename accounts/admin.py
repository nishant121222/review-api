from django.contrib import admin
from .models import User, AdminUser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'name', 'business_id', 'first_seen_at', 'last_seen_at']
    list_filter = ['first_seen_at', 'last_seen_at']
    search_fields = ['phone', 'name']
    readonly_fields = ['first_seen_at', 'last_seen_at']
    fieldsets = (
        (None, {'fields': ('phone', 'name', 'business_id')}),
        ('Metadata', {'fields': ('first_seen_at', 'last_seen_at', 'metadata'), 'classes': ('collapse',)}),
    )


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone', 'role', 'business', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['role', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'phone', 'business__name']
    readonly_fields = ['date_joined']
    fieldsets = (
        ('Login Info', {'fields': ('username', 'email', 'password', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'role', 'groups', 'user_permissions')}),
        ('Business', {'fields': ('business',)}),
        ('Metadata', {'fields': ('date_joined', 'last_login'), 'classes': ('collapse',)}),
    )
