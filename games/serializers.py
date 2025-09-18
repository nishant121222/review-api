# games/serializers.py
from rest_framework import serializers
from .models import Prize, GameResult

class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = ['id', 'code', 'description', 'image_url', 'is_active']


class GameResultSerializer(serializers.ModelSerializer):
    prize = PrizeSerializer()

    class Meta:
        model = GameResult
        fields = ['id', 'user', 'prize', 'created_at', 'redeemed']