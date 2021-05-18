from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_DEFAULT
# Create your models here.

class Ingerdients(models.Model):
    class Types(models.IntegerChoices):
        LIQUID = 1
        SOLID = 2

    ingredient_name = models.CharField(max_length=255)
    type = models.IntegerField(choices=Types.choices)
    class Meta:
        db_table = 'ingredients'


class Units(models.Model):
    unit_name = models.CharField(max_length=255)
    # Ratio to our system default unit
    conventer = models.FloatField()
    class Meta:
        db_table = 'units'

class Recipes(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    last_modification = models.DateTimeField(auto_now_add=True)
    descripction = models.CharField(max_length=511,default=None)
    recipe_name = models.CharField(max_length=255)
    overall_upvotes = models.IntegerField(default=0)
    last_month_upvotes = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    brewing_temperatue = models.FloatField()
    brewing_time = models.FloatField()
    mixing_time = models.FloatField()
    class Meta:
        db_table = 'recipes'

# In db all ammounts will be stored in one type of unit, and will be converted on demand
class IngredientsRecipes(models.Model):
    recipe = models.ForeignKey(Recipes,on_delete=models.CASCADE)
    # Unit in which recipe was created
    unit = models.ForeignKey(Units,on_delete=models.SET_NULL, null=True)
    ammount_in_default_unit = models.FloatField()
    class Meta:
        db_table = 'ingredients_recipes'

class UserSettings(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    liquid_unit = models.ForeignKey(Units,on_delete=models.SET_NULL, null=True,related_name='liquid_unit')
    weight_unit = models.ForeignKey(Units,on_delete=models.SET_NULL, null=True,related_name='weight_unit')
    # If True all recipes will be automaticly converted to choosen units
    default_convert_to_user_unit = models.BooleanField(default=False)
    # If True recipes saved by user will be converted to user choosen units
    default_convert_to_user_unit_on_save = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_settings'
    
class Machines(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    machine_password = models.CharField(max_length=255)

    class Meta:
        db_table = 'machines'
class MachinesStores(models.Model):
    machinie = models.ForeignKey(Machines,on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingerdients,on_delete=models.SET_NULL, null=True)
    # In system default units
    capacity = models.FloatField()
    current_ammount = models.FloatField()

    class Meta:
        db_table = 'machines_stores'

class FavoriteRecipes(models.Model):
    recipe = models.ForeignKey(Recipes,on_delete=CASCADE)
    user = models.ForeignKey(User,on_delete=CASCADE)

    class Meta:
        db_table = 'favorite_recipes'
