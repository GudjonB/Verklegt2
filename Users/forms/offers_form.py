from django.forms import ModelForm, widgets
from Users.models import Offers


class OffersForm(ModelForm):
    class Meta:
        model = Offers
        exclude = ['id']
        widgets = {
            'user': widgets.Select(attrs={'class': 'form-control'}),
            'property': widgets.Select(attrs={'class': 'form-control' }),
            'amount': widgets.NumberInput(attrs={'class': 'form-control' }),
            'expiration': widgets.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime'})
        }
