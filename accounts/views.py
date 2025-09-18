from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer, AdminUserSerializer

# Custom User models
User = get_user_model()  # regular user
AdminUser = get_user_model()  # admin user

# ----------------------------
# ✅ Custom JWT Serializer
# ----------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = getattr(user, "role", None)
        token["business_id"] = user.business.id if getattr(user, "business", None) else None
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "role": getattr(self.user, "role", None),
            "business": getattr(self.user.business, "name", None) if getattr(self.user, "business", None) else None,
        })
        return data

# ----------------------------
# ✅ Custom JWT Login View
# ----------------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ----------------------------
# ✅ Public: Check user by phone
# ----------------------------
class CheckUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        phone = request.query_params.get("phone")
        if not phone:
            return Response({"error": "phone is required"}, status=status.HTTP_400_BAD_REQUEST)
        u = User.objects.filter(phone=phone).first()
        return Response({"returning_user": bool(u), "user_id": u.id if u else None})

# ----------------------------
# ✅ Public: Create regular user
# ----------------------------
class CreateUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        name = request.data.get("name")
        business_id = request.data.get("business_id")

        if not phone:
            return Response({"error": "phone is required"}, status=status.HTTP_400_BAD_REQUEST)

        u, created = User.objects.get_or_create(
            phone=phone,
            defaults={"name": name, "business_id": business_id},
        )
        if not created:
            if name:
                u.name = name
            if business_id:
                u.business_id = business_id
            u.last_seen_at = timezone.now()
            u.save()

        return Response(
            {"id": u.id, "phone": u.phone, "name": u.name, "business_id": u.business_id, "created": created},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

# ----------------------------
# ✅ Public: List all users
# ----------------------------
class ListAllUsersView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

# ----------------------------
# ✅ Protected: Profile
# ----------------------------
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": getattr(user, "role", None),
            "business": getattr(user.business, "name", None) if getattr(user, "business", None) else None,
        })

# ----------------------------
# ✅ Public: Create Admin user from frontend
# ----------------------------
class CreateAdminUserView(APIView):
    permission_classes = [permissions.AllowAny]  # ya aap custom permission set kar sakte ho

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"error": "username, email, and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if AdminUser.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        admin = AdminUser.objects.create_superuser(username=username, email=email, password=password)
        return Response({
            "id": admin.id,
            "username": admin.username,
            "email": admin.email,
            "created": True
        }, status=status.HTTP_201_CREATED)
