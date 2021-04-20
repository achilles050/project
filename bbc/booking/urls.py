from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('checkprice/', views.CheckPrice.as_view()),
    path('checkrange/', views.CheckRange.as_view()),
    path('booking/', views.Booking.as_view()),
    path('payment/', views.Payment.as_view()),
    path('groupbooking/', views.GroupBooking.as_view()),
]
