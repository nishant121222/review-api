from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from businesses.models import Business
from .models import Review
from .services import handle_high_rating_review, handle_approved_review
from drf_yasg.utils import swagger_auto_schema
from .serializers import ReviewSerializer
from django.utils import timezone

User = get_user_model()

# Constants
GOOGLE_LOCATION_ID = "ChIJ9Yw2ruq_wjsRjcPfsQ6gNS8"   # replace with your real location id
SPIN_PAGE_URL = "/games/spin/"


class SubmitReviewView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(security=[])
    def post(self, request):
        user_id = request.data.get("user_id")
        name = request.data.get("name")
        phone = request.data.get("phone")
        business_id = request.data.get("business_id")
        rating = request.data.get("rating")
        comment = request.data.get("comment", "")

        # Validation
        if not (business_id and rating):
            return Response({
                "status": False,
                "message": "business_id and rating are required",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            rating = int(rating)
        except ValueError:
            return Response({
                "status": False,
                "message": "rating must be an integer",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        # ✅ User fetch/create logic
        if user_id:
            user = get_object_or_404(User, id=user_id)
        elif phone:
            user, created = User.objects.get_or_create(
                phone=phone,
                defaults={"username": name or phone}
            )
            if not created and name:
                user.username = name
                user.last_login = timezone.now()
                user.save()
        else:
            return Response({
                "status": False,
                "message": "Either user_id or phone is required",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Business validation
        business = get_object_or_404(Business, id=business_id)

        # ✅ Review creation
        review_status = "published" if rating >= 4 else "pending"
        review = Review.objects.create(
            user=user,
            business=business,
            rating=rating,
            comment=comment,
            status=review_status
        )

        # ✅ Handle WhatsApp notification if high rating
        if rating >= 4:
            try:
                handle_high_rating_review(review)
            except Exception as e:
                print(f"High rating handler error: {e}")

        serializer = ReviewSerializer(review)
        data = serializer.data

        # ✅ Redirect logic
        if rating >= 4:
            data["google_review_link"] = f"https://search.google.com/local/writereview?placeid={GOOGLE_LOCATION_ID}"
            data["spin_page_url"] = SPIN_PAGE_URL
        elif rating == 3:
            data["spin_page_url"] = SPIN_PAGE_URL
        else:
            data["message"] = "Thank you for your feedback!"

        return Response({
            "status": True,
            "message": "Review submitted successfully",
            "data": data
        }, status=status.HTTP_201_CREATED)


class PendingReviewsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(security=[])
    def get(self, request):
        qs = Review.objects.filter(status="pending").order_by("-created_at")
        if not qs.exists():
            return Response({
                "status": False,
                "message": "No Records Found",
                "data": []
            }, status=status.HTTP_200_OK)

        serializer = ReviewSerializer(qs, many=True)
        return Response({
            "status": True,
            "message": "Records Found",
            "data": serializer.data
        })


class ApproveReviewView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(security=[])
    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id, status="pending")
        review.status = "approved"
        review.moderated_by = request.user
        review.save()

        try:
            handle_approved_review(review)
        except Exception as e:
            print(f"Approved review handler failed: {e}")

        serializer = ReviewSerializer(review)
        return Response({
            "status": True,
            "message": "Review approved successfully",
            "data": serializer.data
        })


class RejectReviewView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(security=[])
    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id, status="pending")
        review.status = "rejected"
        review.moderated_by = request.user
        review.save()
        serializer = ReviewSerializer(review)
        return Response({
            "status": True,
            "message": "Review rejected successfully",
            "data": serializer.data
        })
