from django.forms import ModelForm, widgets
from Users.models import Cards


class CardInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CardInfoForm, self).__init__(*args, **kwargs)
        self.fields['expiration'].widget.attrs.update({'class': 'form-control'})  # change expiration class

    class Meta:
        model = Cards
        exclude = ['id']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'user': widgets.HiddenInput(attrs={'class': 'form-control'}, ),
            'number': widgets.TextInput(attrs={'class': 'form-control'}, ),
            'cvc': widgets.TextInput(attrs={'class': 'form-control'}, )
        }
