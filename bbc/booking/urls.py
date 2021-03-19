from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('status/', views.booking.as_view()),
    path('booking/', views.booking.as_view()),
    path('confirm/', views.confirm.as_view()),
]
