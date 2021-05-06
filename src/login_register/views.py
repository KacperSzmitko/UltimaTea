from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import RegisterForm,LoginForm
from django.shortcuts import redirect
from django.contrib.auth import login,logout
from .models import User
# Create your views here.

def home_view(request,*args, **kwargs):

    request.session['lang'] = 'pl'
    register_form = RegisterForm(request.session['lang'],request.POST or None)
    login_form = LoginForm(request.session['lang'],request.POST or None)

    if register_form.is_valid():
        register_form.save()
        response = redirect('/')
        return response

    if login_form.is_valid():
        login_form.save(commit=False)
        remember_me = login_form.cleaned_data['remember_me']
        email_or_login = login_form.cleaned_data['email_or_username']
        if login_form.is_mail:
            login(request,User.objects.get(email=email_or_login))
        else:
            login(request,User.objects.get(username=email_or_login))
        if not remember_me:
                    request.session.set_expiry(0)
        response = redirect('/')
        return response

    is_login = False
    if 'login' in request.POST:
        is_login = True

    context = {
        'register_form':register_form,
        'login_form':login_form,
        'is_login':is_login,
    }
    return render(request,"login_register/login_register.html",context)