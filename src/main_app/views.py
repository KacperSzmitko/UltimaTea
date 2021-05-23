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

def recipes_view(request, *args, **kwargs):
    context = {
        'recipes':[
            {
                'title':'title_val',
                'ing_names':['Sól', 'Sól', 'Sól'],
                'ing_qua':[{'value': 20, 'unit': 'g'},{'value': 20, 'unit': 'g'},{'value': 20, 'unit': 'g'}],
                'tem_name':['Parzenie', 'Grzanie'],
                'tem_val':['95', '2137'],
                'tim_nam':['Parzenie', 'Chłodzenie'],
                'tim_val':[21, 98]
            },
            {
                'title':'title_val',
                'ing_names':['Sól', 'Sól', 'Sól'],
                'ing_qua':[{'value': 20, 'unit': 'g'},{'value': 20, 'unit': 'g'},{'value': 20, 'unit': 'g'}],
                'tem_name':['Parzenie', 'Grzanie'],
                'tem_val':['95', '2137'],
                'tim_nam':['Parzenie', 'Chłodzenie'],
                'tim_val':[21, 98]
            },
            {
                'title':'title_val',
                'ing_names':['Sól', 'Sól', 'Sól'],
                'ing_qua':[{'value': 20, 'unit': 'g'},{'value': 20, 'unit': 'g'},{'value': 20, 'unit': 'g'}],
                'tem_name':['Parzenie', 'Grzanie'],
                'tem_val':['95', '2137'],
                'tim_nam':['Parzenie', 'Chłodzenie'],
                'tim_val':[21, 98]
            },
        ]
    }
    return render(request,"main/recipesList.html", context)