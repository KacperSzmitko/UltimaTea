from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http.request import HttpRequest
from django.urls import reverse
# Create your views here.


def home_view(request, *args, **kwargs):
    context = {
        'title':'Home'
    }
    return render(request,"main/home.html", context)
