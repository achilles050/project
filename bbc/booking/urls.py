from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('status/', views.booking.as_view()),
    path('booking/', views.mybooking),
    path('confirm/', views.confirm),
    path('testcourt/', views.testcourt),
    path('test111/', views.booking.as_view()),
]
