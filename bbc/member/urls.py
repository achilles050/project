from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index),
    path('register/', views.Register),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout),
    path('profile/', views.Profile.as_view()),
    path('listgroup/', views.AllGroup.as_view()),
    path('group/', views.AllGroup.as_view()),
    path('group/<groupname>', views.MyGroup.as_view()),
    path('creategroup/', views.Creategroup.as_view()),

    path('request/', views.Request.as_view()),
    path('mytest/', views.Test),
]
