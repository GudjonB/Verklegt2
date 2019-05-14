from django.forms import ModelForm, widgets
from Users.models import Profiles, User


class StaffForm(ModelForm):
    class Meta:
        model = Profiles
        exclude = ['name', 'address', 'zipCode', 'social', 'image']
        widgets = {
            'user': widgets.Select(attrs={'class': 'form-control'},),
            'id': widgets.HiddenInput()
        }
    def __init__(self,*args,**kwargs):
        super (StaffForm,self ).__init__(*args,**kwargs)
        self.fields['user'].queryset = User.objects.filter(is_staff=False)