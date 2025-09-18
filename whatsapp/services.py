import requests
from django.conf import settings
from .models import WhatsAppLog

def send_whatsapp_message(phone: str, message: str) -> bool:
    token = getattr(settings, 'META_CLOUD_API_TOKEN', '') or ''
    phone_id = getattr(settings, 'META_PHONE_ID', '') or ''

    # For local dev: if not configured, just log success and return True
    if not token or not phone_id:
        WhatsAppLog.objects.create(phone=phone, message=message, status='sent', error='(simulated)')
        return True

    try:
        url = f"https://graph.facebook.com/v19.0/{phone_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {"preview_url": True, "body": message},
        }
        resp = requests.post(url, json=payload, headers={"Authorization": f"Bearer {token}"})
        ok = 200 <= resp.status_code < 300
        WhatsAppLog.objects.create(
            phone=phone,
            message=message,
            status='sent' if ok else 'failed',
            error=None if ok else resp.text
        )
        return ok
    except Exception as e:
        WhatsAppLog.objects.create(phone=phone, message=message, status='failed', error=str(e))
        return False
