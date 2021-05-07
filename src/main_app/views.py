from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.


def home_view(request, *args, **kwargs):

    return HttpResponse("<h1>Zalogowany</h1>")