from django.urls import path
from .views import home_view, recipes_view, machine_info_view

app_name = 'main_app'
urlpatterns = [
    path('', home_view, name='main_home'),
    path('makeTea', home_view, name='main_make_tea'),
    path('editTea', home_view, name='main_edit_tea'),
    path('searchRecipes', home_view, name='main_search_recipes'),
    path('configureIngredients', home_view, name='main_configure_ingredients'),
    path('status', home_view, name='main_status'),
    path('editProfile', home_view, name='main_edit_profile'),

    path('recipesList', recipes_view, name='main_get_recipes'),
    path('machineList', machine_info_view, name='main_get_machine_info')
]
