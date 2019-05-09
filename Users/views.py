from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm

from Users.models import Profiles, CartItems, Favourites
from Properties.models import Properties, Zip

from Users.forms.profile_form import UpdateProfileForm

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
    return render(request, 'Users/profile.html', {
        'Profiles': get_object_or_404(Profiles, pk=Profiles.objects.get(user_id=request.user.id).id)
    })


def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            my_profile = Profiles.objects.get(user_id=request.user.id)
            my_profile.address = form['address'].value()
            my_profile.social = form['social'].value()
            zip_temp = Zip.objects.all().values()
            zip_temp_id_list = []

            for i in zip_temp:
                zip_temp_id_list.append(i['id'])
            if form['zipCode'].value() in zip_temp_id_list:
                zip_id = form['zipCode'].value()
                for j in zip_temp:
                    if zip_id == j['id']:
                        my_profile.zipCode = j['zip']

            my_profile.save()
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'Users/update_profile.html', {
        'form': form
    })


def cart(request):
    Cart = {'Cart': CartItems.objects.filter(user_id=request.user.id)}
    return render(request, 'Users/cart.html', Cart)


def favourites(request):
    context = {'fav': Favourites.objects.filter(user_id=request.user.id)}
    return render(request, 'Users/Favourites.html', context)

