from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .services import send_whatsapp_message  # No need for AdminUser import


class TestSendView(APIView):
    """
    Public – send a test WhatsApp message (no JWT required).
    """
    permission_classes = [permissions.AllowAny]  # Public access

    @swagger_auto_schema(
        security=[],  # removes lock icon in Swagger
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description="Recipient phone number"),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description="Message text"),
            },
            required=['phone']
        ),
        responses={
            200: openapi.Response("Message sent successfully"),
            400: openapi.Response("Bad request (phone missing)"),
            500: openapi.Response("Internal server error"),
        }
    )
    def post(self, request):
        phone = request.data.get('phone')
        message = request.data.get('message', 'Hello from API!')

        if not phone:
            return Response({'error': 'phone is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ok = send_whatsapp_message(phone, message)
            return Response({'sent': ok}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
