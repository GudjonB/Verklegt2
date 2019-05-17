from django.forms import ModelForm, widgets
from Properties.models import OpenHouses, Properties, PropertySellers


class OpenHousesCreateForm(ModelForm):

    class Meta:

        model = OpenHouses
        exclude = ['id']

        widgets = {
            'property': widgets.Select(attrs={'class': 'form-control'}),
            'user': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'length': widgets.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Length in minutes'}),
            'time': widgets.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'dd-mm-yyyy hh:mm'})
        }

    def __init__(self, *args, **kwargs):
        # Access to request inside this form
        self.request = kwargs.pop("request")
        # All properties the current user is selling
        users_properties = PropertySellers.objects.filter(user_id=self.request.user.id)
        tmp_list = []
        # Make tmp_list store all the property id's that the current user is selling in an array
        for i in users_properties:
            tmp_list.append(i.property_id)
        super(OpenHousesCreateForm, self).__init__(*args, **kwargs)
        # Make it so the user can only select properties he is selling
        self.fields['property'].queryset = Properties.objects.filter(deleted=False, pk__in=tmp_list)
