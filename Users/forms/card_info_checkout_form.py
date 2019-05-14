from django.forms import ModelForm, widgets
from Users.models import Cards
from creditcards.forms import CardExpiryField

class CardInfoForm(ModelForm):
    class Meta:
        model = Cards
        exclude = ['id']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'user': widgets.HiddenInput(attrs={'class': 'form-control'}, ),
            'number': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'cvc': widgets.TextInput(attrs={'class': 'form-control'}, )
            #'expiration': widgets.TextInput(attrs={'class': 'form-control'}, ),
        }
        expiration = CardExpiryField(label='Expiration Date')
