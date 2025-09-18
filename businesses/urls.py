# businesses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.business_list, name='business_list'),
    path('<int:business_id>/', views.business_detail, name='business_detail'),
]