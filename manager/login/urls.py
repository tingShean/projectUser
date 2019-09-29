from django.urls import path
from .views import index, add_user


urlpatterns = [
    path('', index),
    path('add_user/', add_user),
]
