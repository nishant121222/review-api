from django.contrib import admin
from .models import WhatsAppLog

@admin.register(WhatsAppLog)
class WhatsAppLogAdmin(admin.ModelAdmin):
    list_display = ['phone', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['phone', 'message']
    readonly_fields = ['phone', 'message', 'status', 'error', 'created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Recipient', {
            'fields': ('phone',)
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('status', 'error')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return False  # Logs are auto-created, not manually added