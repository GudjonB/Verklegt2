from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.utils.datetime_safe import date

from datetime import timedelta
from urllib.parse import urlparse

from Properties.models import Properties, Zip, PropertySellers, PropertyVisits

from Users.models import Profiles, CartItems, Favourites, CheckoutInfo, SearchHistory, User
from Users.forms.offers_form import OffersForm
from Users.forms.profile_form import UpdateProfileForm
from Users.forms.checkout_form import CheckoutInfoForm
from Users.forms.card_info_checkout_form import CardInfoForm
from Users.forms.staff_form import StaffForm

import logging
logger = logging.getLogger(__name__)

def error_404_view(request, exception, template_name="404.html"):
    response = render_to_response("404.html")
    response.status_code = 404
    return response


def error_500_view(request):
    response = render_to_response("404.html")
    response.status_code = 500
    return response


def index(request):
    enddate = date.today()
    monthStartdate = enddate - timedelta(days=30)
    weekStartdate = enddate - timedelta(days=7)
    context = {'Properties': Properties.objects.all().order_by('-id')[:3],
               'Cart': [c.property for c in CartItems.objects.filter(user=request.user.id)],
               'monthVisits': PropertyVisits.objects.filter(date__date__range=[monthStartdate, enddate]).order_by('-counter')[:3],
               'weekVisits': PropertyVisits.objects.filter(date__date__range=[weekStartdate, enddate]).order_by('-counter')[:3],
               'Searches': [s.search for s in SearchHistory.objects.filter(user=request.user).order_by('-id')]}
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
        'selling': PropertySellers.objects.filter(user_id=request.user.id),
        'selling_count': PropertySellers.objects.filter(user_id=request.user.id).count(),
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
    return redirect(request.META.get('HTTP_REFERER'), id)


def remove_from_favourites(request, id):
    favourite = Favourites.objects.filter(property_id=id, user=request.user)
    favourite.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def remove_from_favorites_profile(request, id):
    favourite = Favourites.objects.filter(property_id=id, user=request.user)
    favourite.delete()
    return redirect('profile')


def add_to_cart(request, id):
    item = CartItems(property=get_object_or_404(Properties, pk=id), user=request.user)
    item.save()
    return redirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, id):
    item = CartItems.objects.filter(property_id=id, user=request.user)
    item.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def proceed_to_checkout(request):
    if request.method == 'POST':
        form = CheckoutInfoForm(data=request.POST) #, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('checkoutCardInfo')
    else:
        form = CheckoutInfoForm()
            #initial={'user': request.user,
            #                             'name': request.user.profiles.name,
            #                             'social': request.user.profiles.social
            #                             })
    return render(request, 'Users/checkout.html', {
        'form': form
    })


def read_only_checkout(request):
    read_only = {'info': CheckoutInfo.objects.filter(user_id=request.user.id),
                 'cardInfo': CheckoutInfo.objects.filter(user_id=request.user.id)}
    return render(request, 'Users/read_only_checkout.html', read_only)


def card_info_checkout(request):
    if request.method == 'POST':
        form = CardInfoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('checkoutReadOnly')
    else:
        form = CardInfoForm() # initial={'user': request.user,
                              #       'name': request.user.profiles.name
                              #       })
    return render(request, 'Users/card_info_checkout.html', {
        'form': form
    })


def empty_cart(request):
    items = CartItems.objects.filter(user=request.user)
    for item in items:
        item.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def empty_cart_purchased(request):
    items = CartItems.objects.filter(user=request.user)
    for item in items:
        item.delete()
    return redirect('/')


def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(data=request.POST)
        if form.is_valid:
            user = get_object_or_404(User, pk=form['user'].value())
            user.is_staff = True
            user.save()
    else:
        form = StaffForm()
    return render(request, 'Users/add_staff.html', {
        'form': form
    })
