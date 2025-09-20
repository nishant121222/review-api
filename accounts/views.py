from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer

User = get_user_model()


# ----------------------------
# ✅ Custom JWT Serializer
# ----------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["business_id"] = getattr(user, "business_id", None)
        token["phone"] = getattr(user, "phone", None)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "phone": self.user.phone,
            "business_id": self.user.business_id,
        })
        return data


# ----------------------------
# ✅ JWT Login View
# ----------------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ----------------------------
# ✅ Check user by phone
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
# ✅ Create regular user
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
            defaults={"name": name, "business_id": business_id, "username": phone},
        )

        if not created:
            if name:
                u.name = name
            if business_id:
                u.business_id = business_id
            u.last_seen_at = timezone.now()
            u.save()

        return Response(
            {"status": True, "message": "User created successfully" if created else "User updated",
             "data": {
                 "id": u.id,
                 "phone": u.phone,
                 "name": u.name,
                 "business_id": u.business_id
             }},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


# ----------------------------
# ✅ List all users
# ----------------------------
class ListAllUsersView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        users = User.objects.all()
        if not users.exists():
            return Response({"status": False, "message": "No Records Found", "data": []})
        serializer = UserSerializer(users, many=True)
        return Response({"status": True, "message": "Users fetched successfully", "data": serializer.data})


# ----------------------------
# ✅ Get Latest User
# ----------------------------
class LatestUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        latest_user = User.objects.order_by('-id').values('id', 'username', 'is_superuser').first()
        if latest_user:
            return Response({
                "status": True,
                "message": "Latest user fetched successfully",
                "data": latest_user
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "message": "No user found",
            "data": None
        }, status=status.HTTP_404_NOT_FOUND)


# ----------------------------
# ✅ Protected: Profile
# ----------------------------
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "status": True,
            "message": "Profile fetched successfully",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "business_id": user.business_id,
            }
        })
