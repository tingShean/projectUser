from django.urls import path
from .views import admin_addadmin, admin_dashboard


urlpatterns = [
    path('dashboard/', admin_dashboard),
    path('addadmin/', admin_addadmin),
]
