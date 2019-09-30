from django.urls import path
from .views import user_list, user_cash_log


urlpatterns = [
    path('list/', user_list),
    path('cash_log/', user_cash_log),
]
