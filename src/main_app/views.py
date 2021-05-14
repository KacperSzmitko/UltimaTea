from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http.request import HttpRequest
from django.urls import reverse
# Create your views here.


def home_view(request:HttpRequest):
    if not request.user.is_authenticated:
        return redirect(reverse('login_register:login_register'))
    return HttpResponse("<h1>Zalogowny jako " + request.user.get_username())