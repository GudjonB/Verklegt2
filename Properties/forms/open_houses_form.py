from django.forms import ModelForm, widgets
from Properties.models import OpenHouses, Properties, User


class OpenHousesCreateForm(ModelForm):

    class Meta:

        model = OpenHouses
        exclude = ['id']

        widgets = {
            'property': widgets.Select(attrs={'class': 'form-control'}),
            'user': widgets.Select(attrs={'class': 'form-control'}),
            'length': widgets.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Length in minutes'}),
            'time': widgets.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy hh:mm'})
        }

    def __init__(self, *args, **kwargs):
        super(OpenHousesCreateForm, self).__init__(*args, **kwargs)
        self.fields['property'].queryset = Properties.objects.filter(deleted=False)
        self.fields['user'].queryset = User.objects.filter(is_staff=True)
