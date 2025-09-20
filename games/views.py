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
        cached_prizes = cache.get("prize_list")
        if cached_prizes:
            return Response({'status': True, 'message': 'Prizes fetched successfully', 'data': cached_prizes})

        prizes = Prize.objects.filter(is_active=True).order_by("id")
        if not prizes.exists():
            return Response({'status': False, 'message': 'No Records Found', 'data': []})

        serializer = PrizeSerializer(prizes, many=True)
        cache.set("prize_list", serializer.data, timeout=3600)
        return Response({'status': True, 'message': 'Prizes fetched successfully', 'data': serializer.data})

    except Exception as e:
        return Response({'status': False, 'message': str(e), 'data': []}, status=500)


# -----------------------------
# POST spin wheel (assign random prize)
# -----------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def spin_wheel(request):
    user = request.user
    try:
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if GameResult.objects.filter(user=user, created_at__gte=today_start).exists():
            return Response({'status': False, 'message': 'You have already spun the wheel today', 'data': None}, status=403)

        prizes = list(Prize.objects.filter(is_active=True))
        if not prizes:
            return Response({'status': False, 'message': 'No prizes available', 'data': None}, status=400)

        prize = random.choice(prizes)
        with transaction.atomic():
            game_result = GameResult.objects.create(user=user, prize=prize)

        send_prize_notification.delay(game_result.id)
        serializer = GameResultSerializer(game_result)
        return Response({'status': True, 'message': 'Prize assigned successfully', 'data': serializer.data})

    except Exception as e:
        return Response({'status': False, 'message': str(e), 'data': None}, status=500)


# -----------------------------
# POST redeem prize
# -----------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def redeem_prize(request, result_id: int):
    try:
        with transaction.atomic():
            result = GameResult.objects.select_for_update().get(id=result_id, user=request.user)
            if result.redeemed:
                return Response({'status': False, 'message': 'Already redeemed', 'data': None}, status=400)

            result.redeemed = True
            result.save()

        return Response({'status': True, 'message': 'Prize redeemed successfully', 'data': None})

    except GameResult.DoesNotExist:
        return Response({'status': False, 'message': 'Game result not found', 'data': None}, status=404)
    except Exception as e:
        return Response({'status': False, 'message': str(e), 'data': None}, status=500)
