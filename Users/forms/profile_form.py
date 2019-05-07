from django.forms import ModelForm
from Users.models import Profiles

class ProfileForm(ModelForm):
    class Meta:
        model = Profiles
        exclude = ['id', 'user_id']
        widgets = {
            'test': widgets.Select(attrs={'class': 'form-control'})
        }