from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

from . import views

urlpatterns = [
    path('', views.AdminHome.as_view(), name='home'),
    path('setting/', views.SettingHome.as_view(), name='setting_home'),
    path('setting/allcourt/', views.AllCourtSetting.as_view(),
         name='allcourt_setting'),
    path('setting/<court_number>/', views.EachCourtSetting.as_view(),
         name='eachcourt_setting'),
    path('booking/', views.AdminBooking.as_view(), name='adminbooking'),
    path('member/', views.ListMember.as_view(), name='member'),
    path('member/<pk>', views.DetailMember.as_view(), name='member_detail'),
    path('checkpayment/', views.CheckPayment.as_view(), name='check_payment'),
    path('checkrefund/', views.CheckRefund.as_view(), name='check_refund'),
    path('income_home/', views.IncomeHome.as_view(), name='income_home'),
    path('income/', views.Income.as_view(), name='income'),
]
