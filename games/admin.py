# games/admin.py
from django.contrib import admin
from .models import Prize, GameResult

@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'description', 'is_active')
    search_fields = ('code', 'description')

@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'prize', 'created_at', 'redeemed')
    search_fields = ('user_username', 'prize_code')