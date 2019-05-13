from django.forms import ModelForm, widgets
from Users.models import CheckoutInfo


class CheckoutInfoForm(ModelForm):
    class Meta:
        model = CheckoutInfo
        exclude = ['id', 'user']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'mobile': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'street_name': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'house_number': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'country': widgets.Select(attrs={'class': 'form-control'}, ),
            'city': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'zipCode': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'social': widgets.TextInput(attrs={'class': 'form-control'}, )
        }
