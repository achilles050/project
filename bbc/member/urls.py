from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index),
    path('register/', views.Register),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout),
    path('profile/', views.Profile.as_view()),
    path('listgroup/', views.Listgroup.as_view()),

    path('mygroup/<int:groupid>', views.Mygroup.as_view()),
    path('creategroup/', views.Creategroup.as_view()),
    path('test/', views.Request.as_view()),
    path('test2/', views.testget),
    path('mytest/', views.Test),
]
