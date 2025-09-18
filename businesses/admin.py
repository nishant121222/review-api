from django.contrib import admin
from .models import Business

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'google_location_id', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'google_location_id']
    readonly_fields = ['created_at']
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Google Business Integration', {
            'fields': ('google_location_id',),
            'classes': ('collapse',)
        }),
        ('API Credentials', {
            'fields': ('google_api_creds',),
            'classes': ('collapse',),
            'description': 'Service account JSON. Keep this secure.'
        }),
        ('Settings', {
            'fields': ('settings',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
