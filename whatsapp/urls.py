from django.urls import path
from .views import TestSendView

urlpatterns = [
    path('send/', TestSendView.as_view(), name='whatsapp_send'),  # final URL = /api/whatsapp/send/
]
