from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index),
    path('register/', views.Register),
    path('login/', views.Login),
    path('logout/', views.Logout),
    path('profile/', views.Profile),
]
