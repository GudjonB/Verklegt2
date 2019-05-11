from django.forms import ModelForm, widgets
from Users import models


class StaffForm(ModelForm):
    class Meta:
        model = models.Profiles
        exclude = ['id', 'user', 'address', 'zipCode', 'social', 'image']
        widgets = {
            'name': widgets.Select(attrs={'class': 'form-control'},)
        }
