from django import forms
from django.forms import ModelForm, widgets
from Properties.models import OpenHouses


class OpenHousesCreateForm(ModelForm):

    class Meta:

        model = OpenHouses
        exclude = ['id']
        widgets = {
            'user': widgets.Select(attrs={'class': 'form-control'}),
            'property': widgets.Select(attrs={'class': 'form-control'}),
            'time': widgets.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime'}),
            'length': widgets.NumberInput(attrs={'class': 'form-control'})
        }


