

from datetime import timedelta

from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.utils.datetime_safe import date

from datetime import timedelta
from urllib.parse import urlparse

from Properties.models import Properties, Zip, PropertySellers, PropertyVisits

from Users.models import Profiles, CartItems, Favourites, CheckoutInfo, SearchHistory, User, Cards
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
    searches = []
    cart = []
    if request.user.is_authenticated:
        searches = [s.search for s in SearchHistory.objects.filter(user=request.user).order_by('-id')]
        cart = [c.property for c in CartItems.objects.filter(user=request.user.id)]
    enddate = date.today()
    monthStartdate = enddate - timedelta(days=30)
    weekStartdate = enddate - timedelta(days=7)

    monthvisits = PropertyVisits.objects.filter(property__deleted=False, date__date__range=[monthStartdate, enddate]) \
                      .values('property').annotate(counterSum=Sum('counter')).order_by('-counterSum')[:3]
    for i in monthvisits :
        i['property'] = get_object_or_404(Properties, pk=i['property'])

    context = {'Properties': Properties.objects.filter(deleted=False).order_by('-id')[:3],
               'Cart': cart,
               'monthVisits': monthvisits,
               'weekVisits': PropertyVisits.objects.filter(property__deleted=False, date__date__range=[weekStartdate, enddate]).order_by('-counter')[:3],
               'Searches': searches,
               'User': request.user}
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
    fav = Favourites.objects.filter(user_id=request.user.id, property__in=Properties.objects.filter(deleted=False))
    return render(request, 'Users/profile.html', {
        'Profiles': get_object_or_404(Profiles, pk=Profiles.objects.get(user_id=request.user.id).id),
        'fav': fav,
        'selling': PropertySellers.objects.filter(user_id=request.user.id),
        'selling_count': PropertySellers.objects.filter(user_id=request.user.id).count(),
        'Cart': [c.property for c in CartItems.objects.filter(user=request.user.id)]
    })


def profile_seller(request, id):
    return render(request, 'Users/profile_seller.html', {
        'sellers_profile': get_object_or_404(Profiles, user_id=id),
        'selling': PropertySellers.objects.filter(user_id=id),
        'selling_count': PropertySellers.objects.filter(user_id=id).count()
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
            logger.error(form['image'].value())
            if "/" not in form['image'].value():          # Default image value always contains the whole path
                my_profile.image = form['image'].value()  # Only update if not default image value
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




def cart(request):
    Cart = {'Cart': CartItems.objects.filter(user_id=request.user.id)}
    return render(request, 'Users/cart.html', Cart)


def favourites(request):
    fav = Favourites.objects.filter(user_id=request.user.id, property__in=Properties.objects.filter(deleted=False))
    context = {'fav': fav,
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
        form = CheckoutInfoForm(data=request.POST)
        if form.is_valid():
            print(form)
            form.save()
            return redirect('checkout_card_info')
    else:
        if request.META.get('HTTP_REFERER') == 'http://127.0.0.1:8000/properties/':
            feelingLucky = True
        else:
            feelingLucky = False
        form = CheckoutInfoForm(initial={'user': request.user,
                                         'name': request.user.profiles.name,
                                         'social': request.user.profiles.social,
                                         'feeling_lucky': feelingLucky
                                         })

    return render(request, 'Users/checkout.html', {
        'form': form
    })


def read_only_checkout(request):
    read_only = {'info': CheckoutInfo.objects.filter(user_id=request.user.id).order_by("-id").first(),
                 'cardInfo': Cards.objects.filter(user_id=request.user.id).order_by("-id").first(),
                 'feeling_lucky': CheckoutInfo.objects.filter(user=request.user).order_by('-id').first().feeling_lucky}
    return render(request, 'Users/read_only_checkout.html', read_only)


def card_info_checkout(request):

    if request.method == 'POST':
        form = CardInfoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('checkout_read_only')
    else:
        form = CardInfoForm(initial={'user': request.user})
    return render(request, 'Users/card_info_checkout.html', {
        'form': form
    })


def confirmation_checkout(request):
    total_price = 0
    for i in CartItems.objects.filter(user_id=request.user.id):
        total_price += i.property.price
    confirm = {'items': CartItems.objects.filter(user_id=request.user.id),
               'items_count': CartItems.objects.filter(user_id=request.user.id).count(),
               'total_price': total_price}
    return render(request, 'Users/confirmation_checkout.html', confirm)


def empty_checkout_cancel(request):
    for i in CheckoutInfo.objects.filter(user_id=request.user.id):
        i.delete()
    for i in Cards.objects.filter(user_id=request.user.id):
        i.delete()
    return redirect('cart')



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

def staff(request):
    staff = User.objects.filter(is_staff=True)
    return render(request, 'Users/staff.html', {'staff': staff})

def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(data=request.POST)
        if form.is_valid:
            user = get_object_or_404(User, pk=form['user'].value())
            items = CartItems.objects.filter(user=user)
            for i in items :
                i.delete()
            user.is_staff = True
            user.email = user.username + '@ca.is'
            user.save()
            return redirect('addStaff')
    else:
        form = StaffForm()
    return render(request, 'Users/add_staff.html', {
        'form': form
    })


def about_us(request):
    return render(request, 'Users/about_us.html')
