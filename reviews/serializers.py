from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user_id', 'business_id', 'rating', 'comment', 'status', 'created_at', 'moderated_by']
        read_only_fields = ['status', 'created_at', 'moderated_by']
