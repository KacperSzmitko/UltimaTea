import json
import logging
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http.request import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import FiltersForm, CreateFiltersForm, ChooseIngredient, Profile_form
import logging
import json
import functools
from .models import Recipes, Ingerdients, IngredientsRecipes, Teas,FavoriteRecipes
from django.db.models.query import QuerySet
from django.db.models import Q


def edit_profile_view(request:HttpRequest, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('auth:login_register')
    logger = logging.getLogger('main_logger')

    settings = request.user.usersettings_set.get()
    form = Profile_form(lang='pl')
    if request.method == 'POST': #form.is_valid():#
        logger.info(request.POST)
        logger.info(settings)
        settings.name = request.POST.get('name')
        settings.surname = request.POST.get('surname')
        settings.description = request.POST.get('description')
        settings.save()
    else:
        logger.info("Hej z edit_profile_view!")
        
    form.initial = {'name':settings.name, 'surname':settings.surname, 'description':settings.description}
    context = {
        'title':'Edytuj profil',
        'form': form
    }
    return render(request,"main/edit_profile.html", context)


def edit_machine_view(request:HttpRequest, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('auth:login_register')
    logger = logging.getLogger('main_logger')
    logger.info("Hej z edit_machine_view!")

    if request.method == 'POST' :
        data = json.loads(request.body)
        logger.info(data)

        i = 0
        for container in request.user.machines_set.first().machinecontainers_set.all():
            ing = Ingerdients.objects.get(ingredient_name = data[i])
            container.ingredient = ing
            container.save()
            i+=1

        return HttpResponse(status=200)

    containers = []
    i = 1
    
    for container in request.user.machines_set.first().machinecontainers_set.all():
        actual_choose = ChooseIngredient
        # actual_choose.base_fields['ingredient'].empty_label = container.ingredient.ingredient_name
        containers.append({
            'name':'Pojemnik #{}'.format(i),
            'form':actual_choose(lang='pl', initial = {'ingredient':container.ingredient.id} ),
            'value':container.ammount
        })
        
        # [container.ingredient.ingredient_name, container.ammount])
        i+=1

    context = {
        'title':'Edytuj składniki',
        'containers':containers,
    }
    return render(request,"main/edit_machine.html", context)


def machine_view(request:HttpRequest, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('auth:login_register')
    logger = logging.getLogger('main_logger')
    logger.info("Hej z machine_view!")

    ingredients = []
    for container in request.user.machines_set.first().machinecontainers_set.all():
        ingredients.append([container.ingredient.ingredient_name, container.ammount])

    context = {
        'title':'Machine',
        'ingredients':ingredients,
        'temperatures':[['Komora grzewcza', 87],['Komora parzenia', 27],['Kubek', 24]],
        'valves':[['Pojemnik wody', 'Zamknięty'],['Komora grzewcza', 'Zamknięty'],['Komora parzenia', 'Zamknięty'],['Pojenik składniku #1', 'Zamknięty'],['Pojenik składniku #2', 'Zamknięty'],['Pojenik składniku #3', 'Zamknięty'],['Pojenik składniku #4', 'Zamknięty']],
        'others':[['Wykryto kubek?', 'Tak'],['Kubek pusty?', 'Tak'],['Napięcie zasilania', '12.2 V'],['Napięcie zasilania ESP', '3.3 V'],['Pobór mocy', '2 W'],],

    }
    return render(request,"main/machine.html", context)


def login_required(func):
    def inner(request: HttpRequest):
        if not request.user.is_authenticated:
            return redirect('auth:login_register')
        return func(request)
    return inner

@login_required
def home_view(request:HttpRequest, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('auth:login_register')
    logger = logging.getLogger('main_logger')
    context = {
        'title':'Home'
    }
    return render(request,"main/home.html", context)


@login_required
def edit_recipes_view(request: HttpRequest, *args, **kwargs):
    if request.method == "POST":
        return False

    filters = FiltersForm('pl')
    create_filters = CreateFiltersForm('pl')
    context = {
        'filters': filters,
        'create_filters': create_filters,
    }
    return render(request, "main/edit_recipes.html", context)


@login_required
def browse_recipes_view(request: HttpRequest, *args, **kwargs):
    if request.method == "POST":
        return False

    filters = FiltersForm('pl')
    context = {
        'filters': filters,
    }
    return render(request, "main/browse_recipes.html", context)


def get_main_recipes(request: HttpRequest, *args, **kwargs):
    logger = logging.getLogger('main_logger')
    request_d = json.loads(request.body)

    if request_d['range'] < 0:
        fetched = request.user.recipes_set.filter(
            id__lt=request_d['from']).order_by('-id')[:abs(request_d['range']):-1]
        # logger.info(request_d['range'])
        # logger.info(fetched)
    else:
        fetched = request.user.recipes_set.filter(
            id__gt=request_d['from']).order_by('id')[:request_d['range']]

    recipes_list = []
    for recipe in fetched:
        ing_names = []
        ing_quantity = []

        ing_names.append(recipe.tea_type.tea_name)
        ing_quantity.append({'value': recipe.tea_ammount, 'unit': 'g'})

        ing_names.append('Woda')
        ing_quantity.append({'value': recipe.tea_portion, 'unit': 'g'})

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

    context = {
        'recipes': recipes_list,
        'blank': False,
        'type': 'main',
    }
    return render(request, "main/recipesList.html", context)



def machine_info(request:HttpRequest, *args, **kwargs):
    logger = logging.getLogger('main_logger')

    infos=[]

    for container in request.user.machines_set.first().machinecontainers_set.all():
        infos.append({
            'name':container.ingredient.ingredient_name,
            'value':container.ammount
        })

    context = {
        'infos': infos,
        'username': request.user.username
    }

    return render(request,"main/machineInfo.html", context)


def fetch_edit_recipes(request: HttpRequest, *args, **kwargs):
    recipes, fetched_count = get_recipes(request, 'edit',True)
    context = {
        'recipes': recipes,
        'blank': True,
        'type' : 'edit',
    }
    result = render(
        request, "main/recipesList.html", context)
    result['fetched'] = fetched_count
    result['last_fetch'] = len(recipes)
    return result


def fetch_browse_recipes(request: HttpRequest, *args, **kwargs):
    recipes, fetched_count = get_recipes(request, 'browse',True)
    context = {
        'recipes': recipes,
        'blank': False,
        'type' : 'browse',
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
    if filters['tea_type_filter'] != "":
        recipes = recipes.filter(
            teas__tea_name=filters['tea_type_filter'])

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

# Get recipes, also delete if needed
def get_recipes(request: HttpRequest, type,filters=False):
    request_d = json.loads(request.body)
    fetched_recipes = request_d["fetched_recipes"]
    recipes_to_fetch = request_d["num_of_recipes_to_fetch"]
    filters = request_d["filters"]
    last_fetched = request_d["last_fetch"]
    remove = request_d["remove"]
    id_to_remove = request_d["id_to_remove"]
    recipes_list = []
    user_recipes = ""
    # Edit page
    if type == 'edit':
        # If remove recipe 
        if remove:
            Recipes.objects.get(pk=id_to_remove).delete()

        if filters:
            user_recipes = apply_filters(filters,request.user.recipes_set.all())
        else:
            user_recipes = request.user.recipes_set.all()
    # Browse page
    elif type =='browse':
        if filters:
            user_recipes = apply_filters(
                filters, Recipes.objects.filter(~Q(author = request.user)))
        else:
            user_recipes = Recipes.objects.all(~Q(author=request.user))
    else:
        return Http404()
    # If true returns 0 as fetched
    start_index, end_index = 0,0
    all_user_recipes = len(user_recipes)
    left_recipes = all_user_recipes - fetched_recipes

    if remove:
        # Delete on first page
        if fetched_recipes <= recipes_to_fetch:
            start_index = 0
            # Cant fetch requested number of recipes
            if all_user_recipes <= recipes_to_fetch:
                end_index = all_user_recipes
            # Can fetch requested number of recipes
            else:
                end_index = recipes_to_fetch
        # Delete on >1 page
        else:
            # If deleted was last on page
            if (fetched_recipes - 1) % recipes_to_fetch == 0:
                start_index = fetched_recipes - 1 - recipes_to_fetch
                end_index = start_index + recipes_to_fetch
            else:
                start_index = fetched_recipes - last_fetched
                # There are more recipes in right direction
                if fetched_recipes + 1 <= all_user_recipes:
                    end_index = start_index + last_fetched
                else:
                    end_index = all_user_recipes
    else:
        # Go right
        if recipes_to_fetch > 0:
            # Can fetch
            if left_recipes > 0:
                start_index = fetched_recipes
                end_index = (start_index + 
                    (left_recipes % recipes_to_fetch * (left_recipes < recipes_to_fetch)) +
                    (recipes_to_fetch * (left_recipes >= recipes_to_fetch))
                )
            # Cant fetch
            else:
                start_index = fetched_recipes - last_fetched
                end_index = start_index + last_fetched             
        # Go left
        else:
            # First page
            if fetched_recipes <= abs(recipes_to_fetch):
                start_index = 0
                end_index = start_index + last_fetched
            else:
                end_index = fetched_recipes - last_fetched
                start_index = end_index + recipes_to_fetch



    user_copied_recipes = QuerySet()
    if type == 'browse':
        user_copied_recipes = Recipes.objects.filter(favoriterecipes__user = request.user)
    for recipe in user_recipes[start_index:end_index]:
        ing_names = []
        ing_quantity = []
        
        ing_names.append(recipe.tea_type.tea_name)
        ing_quantity.append({'value': recipe.tea_ammount, 'unit': 'g'})

        ing_names.append('Woda')
        ing_quantity.append({'value': recipe.tea_portion, 'unit': 'g'})

        for ingredient in recipe.ingredientsrecipes_set.all():
            ing_names.append(ingredient.ingredient.ingredient_name)
            ing_quantity.append({'value': ingredient.ammount, 'unit': 'g'})
        copied = False
        if type == 'browse':
            copied = user_copied_recipes.filter(pk=recipe.pk).exists()
        recipes_list.append({
            'id': recipe.id,
            'title': recipe.recipe_name,
            'ing_names': ing_names,
            'ing_qua': ing_quantity,
            'tem_name': ['Parzenie'],
            'tem_val': [recipe.brewing_temperature],
            'tim_nam': ['Parzenie','Mieszanie'],
            'tim_val': [recipe.brewing_time, recipe.mixing_time],
            'favourite': recipe.is_favourite,
            'copied' : copied,
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


def copy_recipe(request: HttpRequest, *args, **kwargs):
    recipe_id = json.loads(request.body)["recipe_id"]
    recipe = Recipes.objects.get(pk=recipe_id)
    FavoriteRecipes.objects.create(user=request.user, recipe=recipe)
    recipe.pk = None
    recipe.author = request.user
    recipe.is_public = False
    recipe.is_favourite = False
    recipe.last_month_upvotes = 0
    recipe.overall_upvotes = 0
    recipe.save()
    return HttpResponse(status=200)

def delete_copied_recipe(request: HttpRequest, *args, **kwargs):
    recipe_id = json.loads(request.body)["recipe_id"]
    recipe = Recipes.objects.get(pk=recipe_id)
    FavoriteRecipes.objects.get(user=request.user, recipe=recipe).delete()
    return HttpResponse(status=200)

# Edit existing recipe or create new recipe
def create_recipe(request: HttpRequest, *args, **kwargs):
    request_d = json.loads(request.body)
    # Edit existing recipe
    if request_d['edit']:
        recipe = Recipes.objects.get(pk=request_d['recipe_id'])
        ings = IngredientsRecipes.objects.filter(recipe=recipe)
        recipe.recipe_name = request_d['recipe_name']
        recipe.brewing_temperature = request_d['brewing_temperature']
        recipe.brewing_time = request_d['brewing_time']
        recipe.mixing_time = request_d['mixing_time']
        recipe.tea_portion = request_d['water']
        recipe.tea_ammount = request_d['tea_quan']
        l = len({k: v for k, v in request_d.items() if 'ingredient' in k})
        # Delete ingredient

        recipe.tea_type = Teas.objects.get(
            pk=request_d['tea_name'])
        for i in range(l):
            if i<3 and request_d[f'ingredient{i+1}'] != '':
                # Non empty value and non empty ingredient
                if request_d[f'ing{i+1}_ammount'] != '':
                    if len(ings) > i:
                        ings[i].ingredient = Ingerdients.objects.get(
                            pk=request_d[f'ingredient{i+1}'])
                        ings[i].ammount = request_d[f'ing{i+1}_ammount']
                        ings[i].save()
                    else:
                        IngredientsRecipes.objects.create(
                            recipe=recipe,
                            ingredient=Ingerdients.objects.get(
                                pk=request_d[f'ingredient{i+1}']),
                            ammount=request_d[f'ing{i+1}_ammount'],
                        )
                # Empty value and non empty ingredenit
                else:
                    ings[i].delete()
            elif i < 3 and request_d[f'ingredient{i+1}'] == '':
                try:
                    ings[i].delete()
                except:
                    pass
        recipe.save()
    # Add new recipe
    else:
        recipe = Recipes.objects.create(author=request.user,
                                        recipe_name=request_d['recipe_name'], 
                                        brewing_temperature=request_d['brewing_temperature'],
                                        brewing_time=request_d['brewing_time'],
                                        mixing_time=request_d['mixing_time'],
                                        tea_portion=request_d['water'],
                                        tea_type=Teas.objects.get(
                                        pk=request_d['tea_name']),
                                        tea_ammount=request_d['tea_quan'],
                            )
        try:
            if request_d['ingredient1'] != '' and request_d['ing1_ammount'] != "":
                IngredientsRecipes.objects.create(
                    recipe=recipe, 
                    ingredient=Ingerdients.objects.get(pk=request_d['ingredient1']),
                    ammount=request_d['ing1_ammount'],
                )
            if request_d['ingredient2'] != '' and request_d['ing2_ammount'] != "":
                IngredientsRecipes.objects.create(
                    recipe=recipe, 
                    ingredient=Ingerdients.objects.get(pk=request_d['ingredient2']),
                    ammount=request_d['ing2_ammount'],
                )
            if request_d['ingredient3'] != '' and request_d['ing3_ammount'] != "":
                IngredientsRecipes.objects.create(
                    recipe=recipe, 
                    ingredient=Ingerdients.objects.get(pk=request_d['ingredient3']),
                    ammount=request_d['ing3_ammount'],
                )
        except Exception :
            recipe.delete()
            return Http404()
    return HttpResponse(status=200)





