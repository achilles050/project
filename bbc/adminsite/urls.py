from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

from . import views

urlpatterns = [
    path('setting/allcourt/<pk>', views.AllCourtSetting.as_view()),
    path('setting/eachcourt/<pk>', views.EachCourtSetting.as_view()),
]
