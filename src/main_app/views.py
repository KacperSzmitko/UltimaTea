import re
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http.request import HttpRequest
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout

import logging
import json

from .models import Recipes, Ingerdients, IngredientsRecipes


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
            'tim_val':[recipe.mixing_time]
        })
    
    context = {
        'recipes': recipes_list
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
    context = {}
    return render(request,"main/edit_recipes.html",context)
