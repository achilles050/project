from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index),
    path('register/', views.Register),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout),
    path('profile/', views.Profile),
    path('listgroup/', views.Listgroup),
    path('mygroup/', views.Mygroup),
    path('creategroup/', views.Creategroup),
    path('test/', views.Request.as_view()),
    path('test2/', views.testget),
]
