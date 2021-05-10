from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
# Create your models here.
class User(AbstractBaseUser):
    username    = models.CharField(max_length=255,unique=True)
    password    = models.CharField(max_length=255)
    email       = models.EmailField(max_length=255,unique=True)    
    is_active   = models.BooleanField(default=False)
    #email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','password']
    class Meta:
        db_table = 'users'

    def get_absolute_url(self):
        return reverse("login_register:login_register")
    