# accounts/serializers.py

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
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["business_id"] = getattr(user, "business_id", None)
        token["phone"] = getattr(user, "phone", None)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Include full user details using UserSerializer
        data["user"] = UserSerializer(self.user).data
        return data
