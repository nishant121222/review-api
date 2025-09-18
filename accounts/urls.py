from django.urls import path
from .views import (
    CheckUserView,
    CreateUserView,
    ListAllUsersView,
    ProfileView,
    CustomTokenObtainPairView,
    CreateAdminUserView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users/', CheckUserView.as_view(), name='check_user'),
    path('users/create/', CreateUserView.as_view(), name='create_user'),
    path('users/all/', ListAllUsersView.as_view(), name='list_all_users'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('admin/create/', CreateAdminUserView.as_view(), name='create_admin_user'),
]
