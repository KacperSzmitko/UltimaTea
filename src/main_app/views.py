import re
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http.request import HttpRequest
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
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
            'tem_val':[recipe.brewing_temperature],
            'tim_nam':['Mieszanie'],
            'tim_val':[recipe.mixing_time],
            'favourite': recipe.is_favourite,
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

    recipes, fetched_count = get_recipes(request, True)
    context = {
        'recipes': recipes,
        'blank': True,
    }
    result = render(
        request, "main/recipesList.html", context)
    result['fetched'] = fetched_count
    result['last_fetch'] = len(recipes)
    return result


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

    if filters['brewing_temperatue_down_filter'] != "":
        if filters['brewing_temperatue_up_filter'] != "":
            recipes = recipes.filter(
                brewing_temperature__gte=filters['brewing_temperatue_down_filter'],
                brewing_temperature__lte=filters['brewing_temperatue_up_filter'])
        else:
            recipes = recipes.filter(
                brewing_temperature__gte=filters['brewing_temperatue_down_filter'])
    elif filters['brewing_temperatue_up_filter'] != "":
        recipes = recipes.filter(
            brewing_temperature__lte=filters['brewing_temperatue_up_filter'])
    
    if filters['brewing_time_down_filter'] != "":
        if filters['brewing_time_up_filter'] != "":
            recipes = recipes.filter(
                brewing_time__gte=filters['brewing_time_down_filter'],
                brewing_time__lte=filters['brewing_time_up_filter'])
        else:
            recipes = recipes.filter(
                brewing_time__gte=filters['brewing_time_down_filter'])
    elif filters['brewing_time_up_filter'] != "":
        recipes = recipes.filter(
            brewing_time__lte=filters['brewing_time_up_filter'])
    
    if filters['mixing_time_down_filter'] != "":
        if filters['mixing_time_up_filter'] != "":
            recipes = recipes.filter(
                mixing_time__gte=filters['mixing_time_down_filter'],
                mixing_time__lte=filters['mixing_time_up_filter'])
        else:
            recipes = recipes.filter(
                mixing_time__gte=filters['mixing_time_down_filter'])
    elif filters['mixing_time_up_filter'] != "":
        recipes = recipes.filter(
            mixing_time__lte=filters['mixing_time_up_filter'])

    return recipes


def get_recipes(request: HttpRequest,filters=False):
    request_d = json.loads(request.body)
    fetched_recipes = request_d["fetched_recipes"]
    recipes_to_fetch = request_d["num_of_recipes_to_fetch"]
    filters = request_d["filters"]
    last_fetched = request_d["last_fetch"]
    remove = request_d["remove"]
    id_to_remove = request_d["id_to_remove"]

    if remove:
        Recipes.objects.get(pk=id_to_remove).delete()

    recipes_list = []

    user_recipes = ""

    if filters:
        user_recipes = apply_filters(filters,request.user.recipes_set.all())
    else:
        user_recipes = request.user.recipes_set.all()

    # If true returns 0 as fetched
    end = False
    # Fetched all
    if len(user_recipes) == fetched_recipes:
        if len(user_recipes) > 0:
            # Last page, Fetched all,  go right
            if recipes_to_fetch > 0:
                start_index = fetched_recipes - last_fetched
                end_index = fetched_recipes
                end = True
            else:
                # First page,Fetched all, go left
                if fetched_recipes <= abs(recipes_to_fetch):
                    start_index = 0
                    end_index = fetched_recipes
                    end = True
    # Not all fetched
    else:
        # First fetch
        if fetched_recipes == 0:
            # If there isnt recipes return 0
            if recipes_to_fetch < 0:
                recipes_to_fetch = 0
            # If there is less than we want to fetch, just fetch all
            elif len(user_recipes) <= recipes_to_fetch:
                recipes_to_fetch = len(user_recipes)
        # Fetch > 1 tell how many recipes left, go right
        elif recipes_to_fetch > 0 and ((len(user_recipes) // fetched_recipes) < 2):
            recipes_to_fetch = len(user_recipes) % fetched_recipes
        # First page , not all fetched ,go left
        elif fetched_recipes <= abs(recipes_to_fetch):
            start_index = 0
            end_index = start_index + abs(recipes_to_fetch)
            end = True

    # Go right
    if not end and recipes_to_fetch >= 0:
        start_index = fetched_recipes
        end_index = fetched_recipes+recipes_to_fetch
    # Go left
    elif not end:
        start_index = fetched_recipes - last_fetched +recipes_to_fetch
        end_index = start_index + abs(recipes_to_fetch)


    for recipe in user_recipes[start_index:end_index]:
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
            'tem_val': [recipe.brewing_temperature],
            'tim_nam': ['Mieszanie'],
            'tim_val': [recipe.mixing_time],
            'favourite': recipe.is_favourite,
        })

    return recipes_list,end_index


def add_to_favourites(request: HttpRequest, *args, **kwargs):
    recipe_id = json.loads(request.body)["recipe_id"]
    recipe = Recipes.objects.get(pk=recipe_id)
    recipe.is_favourite = True
    recipe.save()
    return HttpResponse(status=200)


def delete_from_favourites(request: HttpRequest, *args, **kwargs):
    recipe_id = json.loads(request.body)["recipe_id"]
    recipe = Recipes.objects.get(pk=recipe_id)
    recipe.is_favourite = False
    recipe.save()
    return HttpResponse(status=200)


