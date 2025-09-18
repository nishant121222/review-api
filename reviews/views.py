from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from accounts.models import AdminUser
from businesses.models import Business
from .models import Review
from .services import handle_high_rating_review, handle_approved_review
from drf_yasg.utils import swagger_auto_schema
from .serializers import ReviewSerializer

class SubmitReviewView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(security=[])
    def post(self, request):
        user_id = request.data.get('user_id')
        business_id = request.data.get('business_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment', '')

        if not (user_id and business_id and rating):
            return Response({'error': 'user_id, business_id, rating are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            rating = int(rating)
        except ValueError:
            return Response({'error': 'rating must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(AdminUser, id=user_id)
        business = get_object_or_404(Business, id=business_id)

        review_status = 'published' if rating >= 4 else 'pending'

        review = Review.objects.create(
            user=user,
            business=business,
            rating=rating,
            comment=comment,
            status=review_status
        )

        # Handle WhatsApp notification
        try:
            if rating >= 4:
                handle_high_rating_review(review)
        except Exception as e:
            print(f"High rating handler error: {e}")

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PendingReviewsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(security=[])
    def get(self, request):
        qs = Review.objects.filter(status='pending').order_by('-created_at')
        serializer = ReviewSerializer(qs, many=True)
        return Response(serializer.data)


class ApproveReviewView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(security=[])
    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id, status='pending')
        review.status = 'approved'
        review.moderated_by = request.user
        review.save()

        try:
            handle_approved_review(review)
        except Exception as e:
            print(f"Approved review handler failed: {e}")

        serializer = ReviewSerializer(review)
        return Response(serializer.data)


class RejectReviewView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(security=[])
    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id, status='pending')
        review.status = 'rejected'
        review.moderated_by = request.user
        review.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
