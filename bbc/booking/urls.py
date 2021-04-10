from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('checkrange/', views.CheckRange.as_view()),
    path('booking/', views.Booking.as_view()),
    path('payment/', views.Payment.as_view()),
]
