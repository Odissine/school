from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
]