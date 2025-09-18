# games/services.py
import logging
from celery import shared_task
from whatsapp.services import send_whatsapp_message
from .models import GameResult
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task
def send_prize_notification(game_result_id: int) -> dict:
    """
    Celery task: Sends a WhatsApp message with prize details after a GameResult is created.
    """
    try:
        result = GameResult.objects.get(id=game_result_id)
        user = result.user

        if not getattr(user, "phone", None):
            msg = f"User {user.id} has no phone number, skipping WhatsApp notification."
            logger.warning(msg)
            return {"success": False, "message": msg}

        message = (
            f"🎉 Congratulations!\n"
            f"You've won: {result.prize.description}\n\n"
            f"Show this message at the counter to claim your prize!"
        )

        success = send_whatsapp_message(phone=user.phone, message=message)

        if success:
            msg = f"WhatsApp notification sent successfully to {user.phone}"
            logger.info(msg)
            return {"success": True, "message": msg}
        else:
            msg = f"Failed to send WhatsApp notification to {user.phone}"
            logger.error(msg)
            return {"success": False, "message": msg}

    except GameResult.DoesNotExist:
        msg = f"GameResult with id={game_result_id} does not exist."
        logger.error(msg)
        return {"success": False, "message": msg}

    except Exception as e:
        msg = f"Unexpected error in send_prize_notification: {str(e)}"
        logger.exception(msg)
        return {"success": False, "message": msg}