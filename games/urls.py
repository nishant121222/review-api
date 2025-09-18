# games/urls.py
from django.urls import path
from .views import prize_list, spin_wheel, redeem_prize

urlpatterns = [
    path("prizes/", prize_list, name="prize-list"),
    path("spin/", spin_wheel, name="spin-wheel"),
    path("redeem/<int:result_id>/", redeem_prize, name="redeem-prize"),
]