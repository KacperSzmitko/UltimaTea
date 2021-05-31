from django.urls import path

from .views import *
from django.contrib.auth import views as auth_views

app_name = 'login_register'
urlpatterns = [
    path('',login_view,name='login_register'),
    path('reset_password/',reset_password_view,name='password_reset'),
    path('reset_password_sent/',ResetPasswordSendView.as_view(),name='password_reset_sent'),
    path('reset/<int:id>/<slug:token>/',change_password_view,name='password_change_confirm'),
    path('reset_password_complete/',ResetPasswordCompleteView.as_view(),name='password_change_complete'),
    path('reset_password/invalid/',InvalidLinkView.as_view(),name="invalid_link"),
    path('logout', logout_view,name="logout")
    
]