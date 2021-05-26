import re
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http.request import HttpRequest
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import logging
import json

from .models import Recipes, Ingerdients, IngredientsRecipes


#@login_required(login_url= '/login/')#dev
def home_view(request, *args, **kwargs):
    logger = logging.getLogger('main_logger')
    # logger.info(request.user.recipes_set.all())
    context = {
        'title':'Home'
    }
    return render(request,"main/home.html", context)


def recipes_view(request:HttpRequest, *args, **kwargs):
    logger = logging.getLogger('main_logger')
    recipes_list = []

    for recipe in request.user.recipes_set.all():
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
        # [
        #     {
        #         'id': 28,
        #         'title':'title_val',
        #         'ing_names':['Sól', 'Sól', 'Sól'],
        #         'ing_qua':[{'value': 20, 'unit': 'g'},{'value': 20, 'unit': 'g'},{'value': 20, 'unit': 'g'}],
        #         'tem_name':['Parzenie', 'Grzanie'],
        #         'tem_val':['95', '2137'],
        #         'tim_nam':['Parzenie', 'Chłodzenie'],
        #         'tim_val':[21, 98]
        #     }
        # ]
    }
    
    

    return render(request,"main/recipesList.html", context)