from django.forms import ModelForm, widgets
from Users.models import Cards


class CardInfoForm(ModelForm):
    class Meta:
        model = Cards
        exclude = ['id']
        widgets = {
            'user': widgets.Select(attrs={'class': 'form-control'}, ),
            'number': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'cvc': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'expiration': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'name': widgets.TextInput(attrs={'class': 'form-control'}, )
        }
