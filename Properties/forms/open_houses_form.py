from django.forms import ModelForm, widgets
from Properties.models import OpenHouses, Properties, User, PropertySellers


class OpenHousesCreateForm(ModelForm):

    class Meta:

        model = OpenHouses
        exclude = ['id']

        widgets = {
            'property': widgets.Select(attrs={'class': 'form-control'}),
            'user': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'length': widgets.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Length in minutes'}),
            'time': widgets.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy hh:mm'})
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        users_properties = PropertySellers.objects.filter(user_id=self.request.user.id)
        tmp_list = []
        for i in users_properties:
            tmp_list.append(i.property_id)
        super(OpenHousesCreateForm, self).__init__(*args, **kwargs)
        self.fields['property'].queryset = Properties.objects.filter(deleted=False, pk__in=tmp_list)
