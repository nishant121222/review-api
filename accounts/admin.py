# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # Columns in the list view
    list_display = (
        "id", "username", "phone", "name", "role", "business",
        "is_staff", "is_active", "date_joined", "last_login"
    )
    list_filter = ("role", "is_staff", "is_active", "business")
    search_fields = ("username", "email", "phone", "name")
    ordering = ("id",)

    # Grouped fieldsets in edit form
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("name", "phone", "email", "business")}),
        ("Roles & Permissions", {
            "fields": (
                "role", "is_staff", "is_active", "is_superuser", 
                "groups", "user_permissions"
            )
        }),
        ("Timestamps", {"fields": ("first_seen_at", "last_seen_at", "date_joined", "last_login")}),
    )

    # Fields visible when creating new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "phone", "name", "email", "role",
                "password1", "password2", "is_staff", "is_active"
            ),
        }),
    )

    # Make these fields read-only
    readonly_fields = ("first_seen_at", "last_seen_at", "date_joined", "last_login", "password")
