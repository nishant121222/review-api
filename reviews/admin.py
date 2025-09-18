from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'business', 'rating', 'status', 'created_at', 'moderated_by']
    list_filter = ['status', 'rating', 'business', 'created_at']
    search_fields = ['user__phone', 'comment', 'business__name']
    readonly_fields = ['created_at']
    actions = ['approve_reviews', 'reject_reviews']

    fieldsets = (
        ('Review Details', {
            'fields': ('user', 'business', 'rating', 'comment')
        }),
        ('Status & Moderation', {
            'fields': ('status', 'moderated_by')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def approve_reviews(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='approved',
            moderated_by=request.user
        )
        self.message_user(request, f"{updated} reviews approved.")

    approve_reviews.short_description = "Approve selected pending reviews"

    def reject_reviews(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='rejected',
            moderated_by=request.user
        )
        self.message_user(request, f"{updated} reviews rejected.")

    reject_reviews.short_description = "Reject selected reviews"
        