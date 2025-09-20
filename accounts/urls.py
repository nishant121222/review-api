from django.urls import path
from .views import (
    CheckUserView,
    CreateUserView,
    ListAllUsersView,
    LatestUserView,
    ProfileView,
    CustomTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # 👤 User Management
    path("users/", CheckUserView.as_view(), name="check_user"),
    path("users/create/", CreateUserView.as_view(), name="create_user"),
    path("users/all/", ListAllUsersView.as_view(), name="list_all_users"),
    path("users/latest/", LatestUserView.as_view(), name="latest_user"),

    # 🔑 Auth
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/profile/", ProfileView.as_view(), name="profile"),
]
