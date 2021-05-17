from django.contrib import admin
from django.urls import path, include, reverse_lazy
from . import views


from django.contrib.auth.views import PasswordResetView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


urlpatterns = [

    path('', views.Index.as_view()),
    path('register/', views.Register),
    path('register2/', views.Register2.as_view()),
    path('activate_email/<uidb64>/<token>/',
         views.ActivateEmail.as_view(), name='activate_email'),

    # path('resetpassword/')
    # path('resetpassword/<uidb64>/<token>/'),
    # path('resetpassword/done/'),

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout),
    path('profile/', views.Profile.as_view()),
    path('group/', views.AllGroup.as_view()),
    path('group/<groupname>/', views.MyGroup.as_view()),
    path('creategroup/', views.Creategroup.as_view()),

    path('request/', views.Request.as_view()),
    path('mytest/', views.Test),
    path('test2/', PasswordResetView.as_view(
        template_name="users/password_reset.html"), name="password_reset"),
    path('test3/', PasswordResetView.as_view()),
    # path('test4/', views.password_reset_done, name="password_reset_done")


    path('t/', views.T.as_view()),
]
