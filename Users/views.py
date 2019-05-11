from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm

from Users.forms.offers_form import OffersForm
from Users.models import Profiles, CartItems, Favourites
from Properties.models import Properties
from Users.forms.profile_form import UpdateProfileForm
import logging
logger = logging.getLogger(__name__)


def index(request):
    context = {'Properties': Properties.objects.all().order_by('-id')[:3],
               'Cart': [c.property for c in CartItems.objects.filter(user=request.user.id)]}
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
        'Profiles': get_object_or_404(Profiles, pk=Profiles.objects.get(user_id=request.user.id).id),
        'fav': Favourites.objects.filter(user_id=request.user.id),
        'fav_count': Favourites.objects.filter(user_id=request.user.id).count(),
        'Cart': [c.property for c in CartItems.objects.filter(user=request.user.id)]
    })


def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            my_profile = Profiles.objects.get(user_id=request.user.id)
            my_profile.name = form['name'].value()
            my_profile.address = form['address'].value()
            my_profile.social = form['social'].value()
            my_profile.zipCode_id = form['zipCode'].value()
            my_profile.image = form['image'].value()
            my_profile.save()
            return redirect('profile')
    else:
        profile = Profiles.objects.get(user_id=request.user.id)
        form = UpdateProfileForm(initial={'name': profile.name,
                                          'address': profile.address,
                                          'social': profile.social,
                                          'zipCode': profile.zipCode,
                                          'image': profile.image})
    return render(request, 'Users/update_profile.html', {
        'form': form
    })


def make_offers(request):
    if request.method == 'POST':
        form = OffersForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('propertyDetails')
    else:
        form = OffersForm()
    return render(request, 'Users/make_offers.html', {
        'form': form
    })


def cart(request):
    Cart = {'Cart': CartItems.objects.filter(user_id=request.user.id)}
    return render(request, 'Users/cart.html', Cart)


def favourites(request):
    context = {'fav': Favourites.objects.filter(user_id=request.user.id),
               'Cart': [c.property for c in CartItems.objects.filter(user=request.user.id)]}
    return render(request, 'Users/Favourites.html', context)

def add_to_favourite(request, id):
    favourite = Favourites(property=get_object_or_404(Properties, pk=id), user=request.user)
    favourite.save()
    return redirect("propertyDetails",id)

def remove_from_favourites(request, id):
    favourite = Favourites.objects.filter(property_id=id, user=request.user)
    favourite.delete()
    return redirect('favourites')

def add_to_cart(request, id):
    item = CartItems(property=get_object_or_404(Properties, pk=id), user=request.user)
    item.save()
    return redirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, id):
    item = CartItems.objects.filter(property_id=id, user=request.user)
    item.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def empty_cart(request):
    items = CartItems.objects.filter(user=request.user)
    for item in items:
        item.delete()
    return redirect(request.META.get('HTTP_REFERER'))


