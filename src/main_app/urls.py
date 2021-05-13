from django.urls import path
from .views import home_view

urlpatterns = [
    path('', home_view, name='main_home'),
    path('recipes', home_view, name='main_main_recipes'),
    path('moje_przepisy', home_view, name='main_recipes'),
    path('konfiguracja', home_view, name='main_configuration'),
]
