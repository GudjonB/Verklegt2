from django import forms
from django.forms import ModelForm, widgets
from Properties.models import OpenHouses, Properties, User


class OpenHousesCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(OpenHousesCreateForm, self).__init__(*args, **kwargs)
        self.fields['property'] = forms.ChoiceField(
            choices=Properties.objects.filter(deleted=False).values_list('id', 'address'),
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['user'] = forms.ChoiceField(
            choices=User.objects.filter(is_staff=True).values_list('id', 'username'),
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    class Meta:

        model = OpenHouses
        exclude = ['id']
        widgets = {
            'time': widgets.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime'}),
            'length': widgets.NumberInput(attrs={'class': 'form-control'})
        }
