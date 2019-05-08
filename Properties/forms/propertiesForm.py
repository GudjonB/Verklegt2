from django import forms
from django.forms import ModelForm, widgets
from Properties.models import Properties


SINGLE = 1
DOUBLE = 2
TOWN = 3
MULTI = 4
CASTLE = 5
CAVE = 6
CATEGORIES = [
    (1, "Single Dwelling"),
    (2, "Double Dwelling"),
    (3, "Town House"),
    (4, "Multi Dwelling"),
    (5, "Castle"),
    (6, "Cave")]

class PropertiesCreateForm(ModelForm):

    class Meta:

        model = Properties
        exclude = ['id', 'category_id']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'address': widgets.TextInput(attrs={'class': 'form-control'}),
            'zip': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'category': widgets.Select(attrs={'class': 'form-control'},),
            'size': widgets.TextInput(attrs={'class': 'form-control'}),
            'rooms': widgets.TextInput(attrs={'class': 'form-control'}),
            'bathrooms': widgets.TextInput(attrs={'class': 'form-control'}),
            'year_built': widgets.TextInput(attrs={'class': 'form-control'}),
            'price': widgets.TextInput(attrs={'class': 'form-control'}),
        }
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
