from django.contrib import admin

from .models import Recipes, FavoriteRecipes, IngredientsRecipes, Ingerdients, UserSettings, Machines, History, MachineContainers

admin.site.register(Recipes)
admin.site.register(FavoriteRecipes)
admin.site.register(IngredientsRecipes)
admin.site.register(Ingerdients)
admin.site.register(UserSettings)
admin.site.register(Machines)
admin.site.register(History)
admin.site.register(MachineContainers)