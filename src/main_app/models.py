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


class Teas(models.Model):
    tea_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'teas'


class Recipes(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    last_modification = models.DateTimeField(auto_now_add=True)
    descripction = models.CharField(max_length=1023,default=None)
    recipe_name = models.CharField(max_length=255)
    overall_upvotes = models.IntegerField(default=0)
    last_month_upvotes = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    brewing_temperature = models.FloatField(default=80)
    brewing_time = models.FloatField(default=60)
    mixing_time = models.FloatField(default=15)
    tea_portion = models.FloatField()
    is_favourite = models.BooleanField(default=False)
    tea_type = models.ForeignKey(Teas, on_delete=models.CASCADE)
    class Meta:
        db_table = 'recipes'
        ordering = ('-is_favourite','recipe_name',)

    def __str__(self):
        return self.recipe_name+': '+self.descripction


# In db all ammounts will be stored in one type of unit, and will be converted on demand
class IngredientsRecipes(models.Model):
    recipe = models.ForeignKey(Recipes,on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingerdients,on_delete=models.CASCADE)
    # Unit in which recipe was created
    ammount = models.FloatField()
    class Meta:
        db_table = 'ingredients_recipes'


class UserSettings(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,default='Jan')
    surname = models.CharField(max_length=255,default='Kowalski')
    description = models.CharField(max_length=1000,default='Brak opisu')
    class Meta:
        db_table = 'user_settings'


class Machines(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    machine_password = models.CharField(max_length=255)

    class Meta:
        db_table = 'machines'


class MachineContainers(models.Model):
    machine = models.ForeignKey(Machines, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingerdients, on_delete=models.CASCADE)
    ammount = models.FloatField()

    class Meta:
        db_table = 'machine_container'


class FavoriteRecipes(models.Model):
    recipe = models.ForeignKey(Recipes,on_delete=CASCADE)
    user = models.ForeignKey(User,on_delete=CASCADE)

    class Meta:
        db_table = 'favorite_recipes'


class History(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    recipe = models.ForeignKey(Recipes,on_delete=CASCADE)
    date = models.DateTimeField(auto_now_add=True)
