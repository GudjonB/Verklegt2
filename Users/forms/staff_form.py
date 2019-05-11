from django.forms import ModelForm, widgets
from Users.models import Profiles


class StaffForm(ModelForm):
    class Meta:
        model = Profiles
        exclude = ['name', 'address', 'zipCode', 'social', 'image']
        widgets = {
            'user': widgets.Select(attrs={'class': 'form-control'},),
            'id': widgets.HiddenInput()
        }
