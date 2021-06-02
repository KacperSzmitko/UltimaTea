from django.urls import path
from .views import *

app_name = 'main_app'
urlpatterns = [
    path('', home_view, name='main_home'),
    path('makeTea', home_view, name='main_make_tea'),

    path('editRecipes', edit_recipes_view, name='main_edit_tea'),
    path('browseRecipes', home_view, name='main_search_recipes'),
    path('editIngredients', home_view, name='main_configure_ingredients'),
    path('status', home_view, name='main_status'),
    path('editProfile', home_view, name='main_edit_profile'),



    path('recipesList', recipes_view, name='main_get_recipes'),
    path('machineList', machine_info_view, name='main_get_machine_info'),
    path('fetchRecipesWithFilters', fetch_edit_recipes, name='main_fetch_recipes_with_filters'),
    path('addToFavourites', add_to_favourites,name="main_add_recipe_to_favourites"),
    path('deleteFromFavourites', delete_from_favourites,name="main_delete_recipe_from_favourites"),
]
