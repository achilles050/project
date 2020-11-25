from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('status/', views.court_status),
    path('booking/', views.booking),
    path('confirm/', views.confirm),

]
