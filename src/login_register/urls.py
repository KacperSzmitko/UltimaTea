from django.urls import path

from .views import home_view,remind_view

urlpatterns = [
    path('',home_view,name='login_register'),
    path('remind',remind_view,name='remind'),
]