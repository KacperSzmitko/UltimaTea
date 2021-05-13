from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.


def home_view(request, *args, **kwargs):
    context = {
        'title':'Home'
    }
    return render(request,"main/home.html", context)