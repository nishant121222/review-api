# games/views.py
import random
from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Prize, GameResult
from .serializers import PrizeSerializer, GameResultSerializer
from .services import send_prize_notification


# -----------------------------
# GET list of all active prizes with caching
# -----------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def prize_list(request):
    try:
        # Try fetching from cache first
        cached_prizes = cache.get("prize_list")
        if cached_prizes:
            return Response(cached_prizes)

        # Fetch from database if not cached
        prizes = Prize.objects.filter(is_active=True).order_by("id")
        serializer = PrizeSerializer(prizes, many=True)

        # Store in cache for 1 hour
        cache.set("prize_list", serializer.data, timeout=3600)
        return Response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# -----------------------------
# POST spin wheel (assign random prize)
# -----------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def spin_wheel(request):
    user = request.user

    try:
        # Limit one spin per day per user
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if GameResult.objects.filter(user=user, created_at__gte=today_start).exists():
            return Response({"error": "You have already spun the wheel today."}, status=403)

        prizes = list(Prize.objects.filter(is_active=True))
        if not prizes:
            return Response({"error": "No prizes available"}, status=400)

        prize = random.choice(prizes)

        # Ensure atomic operation to avoid race conditions
        with transaction.atomic():
            game_result = GameResult.objects.create(user=user, prize=prize)

        # Trigger WhatsApp notification asynchronously via Celery
        send_prize_notification.delay(game_result.id)

        serializer = GameResultSerializer(game_result)
        return Response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# -----------------------------
# POST redeem prize
# -----------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def redeem_prize(request, result_id: int):
    try:
        # Atomic update to avoid race conditions during redemption
        with transaction.atomic():
            result = GameResult.objects.select_for_update().get(id=result_id, user=request.user)
            if result.redeemed:
                return Response({"error": "Already redeemed"}, status=400)

            result.redeemed = True
            result.save()

        return Response({"message": "Prize redeemed successfully"})

    except GameResult.DoesNotExist:
        return Response({"error": "Game result not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)