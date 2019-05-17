from django import forms
from django.forms import ModelForm, widgets
from Properties.models import Properties


class PropertiesUpdateForm(ModelForm):

    class Meta:

        model = Properties
        exclude = ['id', 'name', 'deleted', 'image']
        widgets = {
            'address': widgets.TextInput(attrs={'class': 'form-control'}),
            'zip': widgets.Select(attrs={'class': 'form-control'}, ),
            'category': widgets.Select(attrs={'class': 'form-control'}),
            'size': widgets.TextInput(attrs={'class': 'form-control'}),
            'rooms': widgets.TextInput(attrs={'class': 'form-control'}),
            'bathrooms': widgets.TextInput(attrs={'class': 'form-control'}),
            'year_built': widgets.TextInput(attrs={'class': 'form-control'}),
            'price': widgets.TextInput(attrs={'class': 'form-control'})
        }
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
