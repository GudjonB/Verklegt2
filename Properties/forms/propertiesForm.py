from django.forms import ModelForm, widgets
from Properties.models import Properties


class PropertiesCreateForm(ModelForm):
    class Meta:
        model = Properties
        exclude = ['id']
        widgets = {
            'name' : widgets.TextInput(at trs={ 'class': 'form-control'}),

        }