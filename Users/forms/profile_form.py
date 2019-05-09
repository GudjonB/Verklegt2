from django.forms import ModelForm, widgets
from Users.models import Profiles

class ProfileForm(ModelForm):
    class Meta:
        model = Profiles
        exclude = ['id', 'user', 'zipCode']
        widgets = {
            'address': widgets.TextInput(attrs={'class': 'form-control'}),
            'social': widgets.TextInput(attrs={'class': 'form-control' }),
            'image': widgets.TextInput(attrs={'class': 'form-control' })
        }