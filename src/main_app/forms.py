from django.forms.forms import Form
from django import forms
from django.forms.widgets import TextInput
from .models import Ingerdients
from errors import Error, ErrorMessages


class IngerdientsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.ingredient_name

class FiltersForm(forms.Form):
    recipe_name_filter = forms.CharField(max_length=255, required=False,
                                         widget=TextInput(attrs={'class': 'recipe_name_filter filters', 'id': 'recipe_name_filter'}))
    ingredient1_filter = IngerdientsModelChoiceField(
        queryset=Ingerdients.objects.all(), empty_label="Nie wybrano", required=False, 
        widget=forms.Select(attrs={'class': 'filters', 'id': 'id_ing_1'}))
    ingredient2_filter = IngerdientsModelChoiceField(
        queryset=Ingerdients.objects.all(), empty_label="Nie wybrano", required=False,
        widget=forms.Select(attrs={'class': 'filters', 'id': 'id_ing_2'}))
    ingredient3_filter = IngerdientsModelChoiceField(
        queryset=Ingerdients.objects.all(), empty_label="Nie wybrano", required=False,
        widget=forms.Select(attrs={'class': 'filters', 'id': 'id_ing_3'}))
    brewing_temperatue_filter = forms.FloatField(required=False,
        widget=forms.NumberInput(attrs={'class': 'number_filter filters'}))
    brewing_time_filter = forms.FloatField(required=False,
        widget=forms.NumberInput(attrs={'class': 'number_filter filters'}))
    mixing_time_filter = forms.FloatField(required=False,
        widget=forms.NumberInput(attrs={'class': 'number_filter filters'}))

    def __init__(self, lang, *args, **kwargs):
        super(FiltersForm, self).__init__(*args, **kwargs)
        self.message = ErrorMessages.languages[lang]
