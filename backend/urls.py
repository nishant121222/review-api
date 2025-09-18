from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# drf_yasg schema_view
schema_view = get_schema_view(
    openapi.Info(
        title="Review System API",
        default_version='v1',
        description="API documentation for Review System",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # ✅ All public
    authentication_classes=[],  # ✅ empty to remove lock symbols
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # App routes
    path('api/accounts/', include('accounts.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/games/', include('games.urls')),
    path('api/whatsapp/', include('whatsapp.urls')),

    # Add this line
    path('reviewsystem/', include('reviews.urls')),  # ✅ now /reviewsystem/ works

    # Swagger / API docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]
