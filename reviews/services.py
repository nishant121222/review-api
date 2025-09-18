from .google_api import get_google_review_link
from whatsapp.services import send_whatsapp_message

def handle_high_rating_review(review):
    """
    For high ratings (⭐ 4-5), send Google Review link to customer.
    """
    link = get_google_review_link(review.business)
    if link:
        msg = f"Thanks for your {review.rating}★ feedback! Please share it publicly here: {link}"
        send_whatsapp_message(review.user.phone, msg)

def handle_approved_review(review):
    """
    For low ratings after admin approval, notify customer to post on Google.
    """
    link = get_google_review_link(review.business)
    if link:
        msg = f"Your review has been approved ✅. Publish it here: {link}"
        send_whatsapp_message(review.user.phone, msg)
