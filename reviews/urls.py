from django.urls import path
from .views import SubmitReviewView, PendingReviewsView, ApproveReviewView, RejectReviewView

urlpatterns = [
    path('', SubmitReviewView.as_view(), name='reviews-submit'),
    path('pending/', PendingReviewsView.as_view(), name='reviews-pending'),
    path('<int:review_id>/approve/', ApproveReviewView.as_view(), name='reviews-approve'),
    path('<int:review_id>/reject/', RejectReviewView.as_view(), name='reviews-reject'),
]
