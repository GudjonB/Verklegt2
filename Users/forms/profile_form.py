from django.forms import ModelForm, widgets
from Users.models import Profiles


class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profiles

        exclude = ['id', 'user']  # TODO: image AND zipCode
        widgets = {
            'address': widgets.TextInput(attrs={'class': 'form-control'}),
            'social': widgets.TextInput(attrs={'class': 'form-control'}),
            'image': widgets.FileInput(attrs={'class': 'form-control'}, ),

            'zipCode': widgets.TextInput(attrs={'class': 'form-control'})
            # 'image': widgets.TextInput(attrs={'class': 'form-control'})
        }
