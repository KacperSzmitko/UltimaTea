from django.urls import path
from .views import *

app_name = 'main_app'
urlpatterns = [
    path('', home_view, name='main_home'),
    path('makeTea', home_view, name='main_make_tea'),

    path('editRecipes', edit_recipes_view, name='main_edit_tea'),
    path('browseRecipes', browse_recipes_view, name='main_browse_recipes'),
    path('editIngredients', home_view, name='main_configure_ingredients'),
    path('status', home_view, name='main_status'),
    path('editProfile', home_view, name='main_edit_profile'),

    path('recipesList', get_main_recipes, name='main_get_recipes'),
    path('machineList', machine_info, name='main_get_machine_info'),
    path('fetchRecipesWithFilters', fetch_edit_recipes, name='main_fetch_recipes_with_filters'),
    path('addToFavourites', add_to_favourites,name="main_add_recipe_to_favourites"),
    path('deleteFromFavourites', delete_from_favourites,name="main_delete_recipe_from_favourites"),
    path('copyRecipe', copy_recipe,
         name="main_copy_recipe"),
    path('deleteCopiedRecipe', delete_copied_recipe,
         name="main_delete_copied_recipe"),
    path('createRecipe', create_recipe,name="main_create_recipe"),
    path('browseFetchRecipesWithFilters', fetch_browse_recipes,name='main_fetch_recipes_with_filters_browse'),
]
