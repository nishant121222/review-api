from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, AdminUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'name', 'business_id', 'first_seen_at', 'last_seen_at']


class AdminUserSerializer(serializers.ModelSerializer):
    business = serializers.CharField(source='business.name', read_only=True)

    class Meta:
        model = AdminUser
        fields = ['id', 'username', 'email', 'role', 'business']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extend default JWT to include admin user details in the response.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = AdminUserSerializer(self.user).data
        return data
