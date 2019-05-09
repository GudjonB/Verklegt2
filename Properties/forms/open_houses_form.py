from django import forms
from django.forms import ModelForm, widgets
from Properties.models import OpenHouses


class PropertiesCreateForm(ModelForm):

    class Meta:

        model = OpenHouses
        exclude = ['id']
        widgets = {
            'property': widgets.Select(attrs={'class': 'form-control'}),
            'time': widgets.Select(attrs={'class': 'form-control'}),
        }
