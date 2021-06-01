import re
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http.request import HttpRequest
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .models import Ingerdients
from django.contrib.auth import logout
from .forms import FiltersForm
import logging
import json
import functools
from .models import Recipes, Ingerdients, IngredientsRecipes
from django.db.models.query import QuerySet

#@login_required()
def home_view(request:HttpRequest, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('auth:login_register')
    logger = logging.getLogger('main_logger')
    context = {
        'title':'Home'
    }
    return render(request,"main/home.html", context)


def recipes_view(request:HttpRequest, *args, **kwargs):
    logger = logging.getLogger('main_logger')
    request_d = json.loads(request.body)

    
    if request_d['range'] < 0:
        fetched = request.user.recipes_set.filter(id__lt = request_d['from']).order_by('-id')[:abs(request_d['range']):-1]
        # logger.info(request_d['range'])
        # logger.info(fetched)
    else:
        fetched = request.user.recipes_set.filter(id__gt = request_d['from']).order_by('id')[:request_d['range']]
    
    recipes_list = []
    for recipe in fetched:
        ing_names = []
        ing_quantity = []

        for ingredient in recipe.ingredientsrecipes_set.all():
            ing_names.append(ingredient.ingredient.ingredient_name)
            ing_quantity.append({'value': ingredient.ammount, 'unit': 'g'})
        
        recipes_list.append({
            'id': recipe.id,
            'title':recipe.recipe_name,
            'ing_names':ing_names,
            'ing_qua':ing_quantity,
            'tem_name':['Parzenie'],
            'tem_val':[recipe.brewing_temperatue],
            'tim_nam':['Mieszanie'],
            'tim_val':[recipe.mixing_time],
        })
    
    context = {
        'recipes': recipes_list,
        'blank': False,
    }

    return render(request,"main/recipesList.html", context)


def machine_info_view(request:HttpRequest, *args, **kwargs):
    logger = logging.getLogger('main_logger')

    infos=[]

    for container in request.user.machines_set.first().machinecontainers_set.all():
        infos.append({
            'name':container.ingredient.ingredient_name,
            'value':container.ammount
        })

    context = {
        'infos': infos
    }

    return render(request,"main/machineInfo.html", context)


def edit_recipes_view(request: HttpRequest, *args, **kwargs):



    if request.method == "POST":
        return True

    filters = FiltersForm('pl')
    context = {
        'filters': filters,
    }
    return render(request,"main/edit_recipes.html",context)

# Get n objects and apply filters
def fetch_edit_recipes(request: HttpRequest, *args, **kwargs):

    context = {
        'recipes': get_recipes(request,True),
        'blank': True,
    }
    return render(request, "main/recipesList.html", context)


def apply_filters(filters, recipes: QuerySet):

    if filters['recipe_name_filter'] != "":
        recipes = recipes.filter(
            recipe_name__iregex=f".*(?={filters['recipe_name_filter']}).*")
    if filters['ingredient1_filter'] != "":
        recipes = recipes.filter(
            ingredientsrecipes__ingredient__ingredient_name=filters['ingredient1_filter'])
    if filters['ingredient2_filter'] != "":
        recipes = recipes.filter(
            ingredientsrecipes__ingredient__ingredient_name=filters['ingredient2_filter'])
    if filters['ingredient3_filter'] != "":
        recipes = recipes.filter(
            ingredientsrecipes__ingredient__ingredient_name=filters['ingredient3_filter'])
    if filters['brewing_temperatue_filter'] != "":
        recipes = recipes.filter(
            brewing_temperatue=filters['brewing_temperatue_filter'])
    if filters['brewing_time_filter'] != "":
        recipes = recipes.filter(
            brewing_time=filters['brewing_time_filter'])
    if filters['mixing_time_filter'] != "":
        recipes = recipes.filter(
            mixing_time=filters['mixing_time_filter'])
    return recipes


def get_recipes(request: HttpRequest,filters=False):
    request_d = json.loads(request.body)
    fetched_recipes = request_d["fetched_recipes"]
    recipes_to_fetch = request_d["num_of_recipes_to_fetch"]
    filters = request_d["filters"]
    recipes_list = []

    user_recipes = ""

    if filters:
        user_recipes = apply_filters(filters,request.user.recipes_set.all())
    else:
        user_recipes = request.user.recipes_set.all()

    # Cannot fetch given number of recipes
    if fetched_recipes == 0:
        # If there is less than we want to fetch, just fetch all
        if len(user_recipes) <= recipes_to_fetch:
            recipes_to_fetch = len(user_recipes)
    elif ((len(user_recipes) // fetched_recipes) < 2):
        recipes_to_fetch = len(user_recipes) % fetched_recipes

    for recipe in user_recipes[fetched_recipes:fetched_recipes+recipes_to_fetch]:

        ing_names = []
        ing_quantity = []

        for ingredient in recipe.ingredientsrecipes_set.all():
            ing_names.append(ingredient.ingredient.ingredient_name)
            ing_quantity.append({'value': ingredient.ammount, 'unit': 'g'})

        recipes_list.append({
            'id': recipe.id,
            'title': recipe.recipe_name,
            'ing_names': ing_names,
            'ing_qua': ing_quantity,
            'tem_name': ['Parzenie'],
            'tem_val': [recipe.brewing_temperatue],
            'tim_nam': ['Mieszanie'],
            'tim_val': [recipe.mixing_time],
        })
    return recipes_list
