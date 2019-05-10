from django.forms import ModelForm, widgets
from Properties.models import PropertyImages


class PropertiesImagesForm(ModelForm):
    class Meta:
        model = PropertyImages
        exclude = ['id']
        widgets = {
            'property': widgets.Select(attrs={'class': 'form-control'}, ),
            'image': widgets.FileInput(attrs={'class': 'form-control'}, )
        }
