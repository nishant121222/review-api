from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    business = serializers.CharField(source='business.name', read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "phone", "name",
            "business", "role", "first_seen_at", "last_seen_at"
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extend default JWT to include user details in the response.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data
