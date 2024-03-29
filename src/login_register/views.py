from re import template
from django.db import models
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator 
from django.conf import settings
from .tasks import send_mails
import time
import logging
from main_app.models import Machines, MachineContainers, Ingerdients, UserSettings

def login_view(request:HttpRequest,*args, **kwargs):
    register_form = RegisterForm('pl',request.POST or None)
    login_form = LoginForm('pl',request.POST or None)
    # Tells which form was submited. Empty string on get
    is_login = False
    is_register = False

    if 'login' in request.POST:
        is_login = True
    elif 'register' in request.POST:
        is_register = True


    if is_register and register_form.is_valid():
        register_form.save()
        new_user = User.objects.filter(username = register_form.cleaned_data.get("username")).first()
        new_machine = Machines(user = new_user, machine_password='12345')
        new_container1 = MachineContainers(machine = new_machine, ingredient = Ingerdients.objects.filter(id = 1).first(), ammount = 0)
        new_container2 = MachineContainers(machine = new_machine, ingredient = Ingerdients.objects.filter(id = 1).first(), ammount = 0)
        new_container3 = MachineContainers(machine = new_machine, ingredient = Ingerdients.objects.filter(id = 1).first(), ammount = 0)
        new_container4 = MachineContainers(machine = new_machine, ingredient = Ingerdients.objects.filter(id = 1).first(), ammount = 0)
        new_container5 = MachineContainers(machine = new_machine, ingredient = Ingerdients.objects.filter(id = 1).first(), ammount = 0)
        user_desc = UserSettings(user = new_user)
        new_machine.save()
        new_container1.save()
        new_container2.save()
        new_container3.save()
        new_container4.save()
        new_container5.save()
        user_desc.save()
        register_form = RegisterForm('pl')
        



    if is_login and login_form.is_valid():
        remember_me = login_form.cleaned_data['remember_me']
        username = request.POST.get('login_username')
        try:
            username = User.objects.get(email=username).username
        except:
            username = User.objects.get(username=username).username
        user = authenticate(request,username=username,password=request.POST.get('password'))
        if user is not None:
            login(request,user)
        if not remember_me:
            request.session.set_expiry(0)
        return  redirect(reverse('app:main_home'))


    context = {
        'register_form':register_form,
        'login_form':login_form,
        'is_login':is_login,
        'is_register':is_register,
    }

    #send_mail("Test","Wiadomość",'UltimaTeaService@gmail.com',["kacperszmitk@wp.pl"])
    return render(request,"login_register/login_register.html",context)

    
def reset_password_view(request:HttpRequest):

    reset_password_form = ResetPasswordForm('pl')
    if request.method == 'POST':
        reset_password_form = ResetPasswordForm('pl',request.POST)
        if reset_password_form.is_valid():
            user = User.objects.get(email=reset_password_form.cleaned_data['email'])
            token = default_token_generator.make_token(user)
            context = {
                'id': user.id,
                'token':token,
                'adr':request.META.get("HTTP_HOST")
            }
            send_mails.delay(
                context, reset_password_form.cleaned_data['email'])

            return redirect(reverse("auth:password_reset_sent"))
    
    context = {
        'reset_password_form':reset_password_form
    }
    return render(request,"login_register/password_reset.html",context)


class ResetPasswordSendView(TemplateView):
    template_name = "login_register/password_reset_sent.html"

class InvalidLinkView(TemplateView):
    template_name = "login_register/invalid_link.html"


def change_password_view(request:HttpRequest, *args, **kwargs):


    change_password_form = ChangePasswordForm('pl', request.POST or None)
    if not User.objects.filter(id=kwargs.get("id")).exists() or not default_token_generator.check_token(User.objects.get(id=kwargs.get("id")), kwargs.get("token")):
        return redirect(reverse("auth:invalid_link"))

    if change_password_form.is_valid():
        user = User.objects.get(id=kwargs.get("id"))
        user.set_password(change_password_form.cleaned_data.get("password"))
        user.save()
        return redirect(reverse("auth:password_change_complete"))

    context = {
        'change_password_form':change_password_form,
    }
    return render(request,"login_register/password_change.html",context)
    
class ResetPasswordCompleteView(TemplateView):
    template_name = 'login_register/password_change_complete.html'
    

def logout_view(request:HttpRequest, *args, **kwargs):
    logout(request)
    return  redirect(reverse('auth:login_register'))

