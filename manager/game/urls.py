from django.urls import path
from .views import game_active, game_notice, pvp_active


urlpatterns = [
    path('active/', game_active),
    path('notice/', game_notice),
    path('pvp_active', pvp_active),
]