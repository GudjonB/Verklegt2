from django.forms import ModelForm, widgets
from Users.models import Profiles

class ProfileForm(ModelForm):
    class Meta:
        model = Profiles
        exclude = ['id', 'user', 'zipCode', 'social']
        widgets = {
            'change_info': widgets.Select(attrs={'class': 'form-control' }),
            'profile_image': widgets.TextInput(attrs={'class': 'form-control' })
        }