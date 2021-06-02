from django.forms.forms import Form
from django import forms
from django.forms.widgets import Select, TextInput
from .models import Ingerdients,Teas
from errors import Error, ErrorMessages


class IngerdientsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.ingredient_name


class TeaNamesChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.tea_name

class FiltersForm(forms.Form):
    recipe_name_filter = forms.CharField(max_length=255, required=False,
        widget=TextInput(attrs={'class': 'recipe_name_filter filters', 'id': 'recipe_name_filter'}))
    tea_name_filter = TeaNamesChoiceField(queryset=Teas.objects.all(), empty_label="Nie wybrano", required=False,
        widget=forms.Select(attrs={'class': 'tea_name_filter filters choice', 'id': 'tea_name_filter'}))
    ingredient1_filter = IngerdientsModelChoiceField(
        queryset=Ingerdients.objects.all(), empty_label="Nie wybrano", required=False, 
        widget=forms.Select(attrs={'class': 'filters choice', 'id': 'id_ing_1'}))
    ingredient2_filter = IngerdientsModelChoiceField(
        queryset=Ingerdients.objects.all(), empty_label="Nie wybrano", required=False,
        widget=forms.Select(attrs={'class': 'filters choice', 'id': 'id_ing_2'}))
    ingredient3_filter = IngerdientsModelChoiceField(
        queryset=Ingerdients.objects.all(), empty_label="Nie wybrano", required=False,
        widget=forms.Select(attrs={'class': 'filters choice', 'id': 'id_ing_3'}))
    brewing_temperatue_down_filter = forms.FloatField(required=False,
        widget=forms.NumberInput(attrs={'class': 'number_filter filters'}))
    brewing_time_down_filter = forms.FloatField(required=False,
        widget=forms.NumberInput(attrs={'class': 'number_filter filters'}))
    mixing_time_down_filter = forms.FloatField(required=False,
        widget=forms.NumberInput(attrs={'class': 'number_filter filters'}))
    brewing_temperatue_up_filter = forms.FloatField(required=False,
        widget=forms.NumberInput(attrs={'class': 'number_filter filters'}))
    brewing_time_up_filter = forms.FloatField(required=False,
        widget=forms.NumberInput(attrs={'class': 'number_filter filters'}))
    mixing_time_up_filter = forms.FloatField(required=False,
        widget=forms.NumberInput(attrs={'class': 'number_filter filters'}))
    

    def __init__(self, lang, *args, **kwargs):
        super(FiltersForm, self).__init__(*args, **kwargs)
        self.message = ErrorMessages.languages[lang]


class CreateFiltersForm(forms.Form):
    recipe_name = forms.CharField(max_length=255, required=False,
                                  widget=TextInput(attrs={'class': 'recipe_name create text_input', 'id': 'recipe_name_create'}))
    water = forms.FloatField(max_value=150,required=False, 
                                                widget=forms.NumberInput(attrs={'class': 'number create'}))
    tea_name_filter = TeaNamesChoiceField(queryset=Teas.objects.all(), empty_label="Nie wybrano", required=False,
                                    widget=forms.Select(attrs={'class': 'tea_name choice', 'id': 'tea_name_create'}))
    ingredient1 = IngerdientsModelChoiceField(
        queryset=Ingerdients.objects.all(), empty_label="Nie wybrano", required=False, 
        widget=forms.Select(attrs={'class': 'create choice', 'id': 'id_ing_1_create'}))
    ingredient2 = IngerdientsModelChoiceField(
        queryset=Ingerdients.objects.all(), empty_label="Nie wybrano", required=False,
        widget=forms.Select(attrs={'class': 'create choice', 'id': 'id_ing_2_create'}))
    ingredient3 = IngerdientsModelChoiceField(
        queryset=Ingerdients.objects.all(), empty_label="Nie wybrano", required=False,
        widget=forms.Select(attrs={'class': 'create choice', 'id': 'id_ing_3_create'}))
    ing1 = forms.FloatField(required=False,max_value=150,
                                               widget=forms.NumberInput(attrs={'class': 'number create'}))
    ing2 = forms.FloatField(required=False,max_value=150,
                                               widget=forms.NumberInput(attrs={'class': 'number create'}))
    ing3 = forms.FloatField(required=False,max_value=150,
                                               widget=forms.NumberInput(attrs={'class': 'number create'}))
    tea_quan = forms.FloatField(required=False,max_value=150,
                                               widget=forms.NumberInput(attrs={'class': 'number create'}))                                           
    
    brewing_temperatue = forms.FloatField(required=False,max_value=150,
                                               widget=forms.NumberInput(attrs={'class': 'number create'}))
    brewing_time = forms.FloatField(required=False,
                                         widget=forms.NumberInput(attrs={'class': 'number create'}))
    mixing_time = forms.FloatField(required=False,
                                        widget=forms.NumberInput(attrs={'class': 'number create'}))
    

    def __init__(self, lang, *args, **kwargs):
        super(CreateFiltersForm, self).__init__(*args, **kwargs)
        self.message = ErrorMessages.languages[lang]
