from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm

from Users.forms.profile_form import ProfileForm
from Users.models import Profiles
from Properties.models import Properties, Zip
import logging
logger = logging.getLogger(__name__)
# logger.error(form['address'].value())


def index(request):
    context = {'Properties': Properties.objects.all().order_by('-id')}
    return render(request, 'Users/index.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            new_profile = Profiles(user=new_user)
            new_profile.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'Users/register.html', {
        'form': form
    })


def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            my_profile = Profiles.objects.get(user_id=request.user.id)
            my_profile.address = form['address'].value()
            my_profile.social = form['social'].value()
            # my_profile.zipCode = form['zipCode'].data

            my_profile.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'Users/profile.html', {
        'form': form
    })
