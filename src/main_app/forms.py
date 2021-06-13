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
    recipe_name = forms.CharField(max_length=255,
                                  widget=TextInput(attrs={'class': 'recipe_name create text_input', 'id': 'recipe_name_create'}))
    water = forms.FloatField(max_value=250, 
                                                widget=forms.NumberInput(attrs={'class': 'number_edit create'}))
    tea_name = TeaNamesChoiceField(queryset=Teas.objects.all(), empty_label="Nie wybrano",
                                    widget=forms.Select(attrs={'class': 'tea_name choice_edit', 'id': 'tea_name_create'}))
    ingredient1 = IngerdientsModelChoiceField(
        queryset=Ingerdients.objects.all(), empty_label="Nie wybrano", required=False, 
        widget=forms.Select(attrs={'class': 'create choice_edit', 'id': 'id_ing_1_create'}))
    ingredient2 = IngerdientsModelChoiceField(
        queryset=Ingerdients.objects.all(), empty_label="Nie wybrano", required=False,
        widget=forms.Select(attrs={'class': 'create choice_edit', 'id': 'id_ing_2_create'}))
    ingredient3 = IngerdientsModelChoiceField(
        queryset=Ingerdients.objects.all(), empty_label="Nie wybrano", required=False,
        widget=forms.Select(attrs={'class': 'create choice_edit', 'id': 'id_ing_3_create'}))
    ing1_ammount = forms.FloatField(required=False,max_value=150,
                                               widget=forms.NumberInput(attrs={'class': 'number_edit create'}))
    ing2_ammount = forms.FloatField(required=False, max_value=150,
                                               widget=forms.NumberInput(attrs={'class': 'number_edit create'}))
    ing3_ammount = forms.FloatField(required=False, max_value=150,
                                               widget=forms.NumberInput(attrs={'class': 'number_edit create'}))
    tea_quan = forms.FloatField(required=False,max_value=500,
                                               widget=forms.NumberInput(attrs={'class': 'number_edit create'}))                                           
    
    brewing_temperature = forms.FloatField(max_value=150,
                                               widget=forms.NumberInput(attrs={'class': 'number_edit create'}))
    brewing_time = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'number_edit create'}))
    mixing_time = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'number_edit create'}))
    

    def __init__(self, lang, *args, **kwargs):
        super(CreateFiltersForm, self).__init__(*args, **kwargs)
        self.message = ErrorMessages.languages[lang]


class ChooseIngredient(forms.Form):
    ingredient = IngerdientsModelChoiceField(
        queryset=Ingerdients.objects.all(), empty_label="Pusty", required=False, 
        widget=forms.Select(attrs={'class': 'choose'}))
    
    def __init__(self, lang, *args, **kwargs):
        super(ChooseIngredient, self).__init__(*args, **kwargs)
        self.message = ErrorMessages.languages[lang]



class Profile_form(forms.Form):
    name = forms.CharField(max_length=255, required=True,
        widget=TextInput(attrs={'class': 'nameField input'}))
    surname = forms.CharField(max_length=255, required=True,
        widget=TextInput(attrs={'class': 'surnameField input'}))
    description = forms.CharField(max_length=1000, required=False,
        widget=forms.Textarea(attrs={'class': 'descriptionField input', 'rows':4, 'cols':25}))
    
    def __init__(self, lang, *args, **kwargs):
        super(Profile_form, self).__init__(*args, **kwargs)
        self.message = ErrorMessages.languages[lang]