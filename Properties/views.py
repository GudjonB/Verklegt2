from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum

from Properties.forms.properties_form import PropertiesCreateForm
from Properties.forms.properties_form_update import PropertiesUpdateForm
from Properties.forms.open_houses_form import OpenHousesCreateForm
from Properties.forms.properties_images_form import PropertiesImagesForm
from Properties.models import *
from Users.models import CartItems, Favourites, SearchHistory, Cards
from Helpers.getData import clearFiles, writeToCsv, readFromCsv
from datetime import datetime
import logging
import urllib
import random

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'Properties/index.html')


@login_required
def create_properties(request):
    if request.method == 'POST':
        form = PropertiesCreateForm(request.POST, request.FILES)
        if form.is_valid():
            properties = form.save()
            description = Description(description=request.POST['description'], property=properties)
            description.save()
            sellers = PropertySellers(user_id=request.user.id, property_id=properties.id)
            sellers.save()
            if form.cleaned_data['image']:
                images = PropertyImages(image=form.cleaned_data['image'], property_id=properties.id)
                images.save()
            return redirect('all_properties')
    else:
        form = PropertiesCreateForm()
    return render(request, 'Properties/create_properties.html', {
        'form': form
    })


@login_required
def update_property(request, id):
    if request.method == 'POST':
        form = PropertiesUpdateForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            property_to_update = get_object_or_404(Properties, pk=id)
            description_to_update = get_object_or_404(Description, property_id=id)

            property_to_update.address = form['address'].value()
            property_to_update.zip_id = form['zip'].value()
            property_to_update.category_id = form['category'].value()
            property_to_update.size = form['size'].value()
            property_to_update.rooms = form['rooms'].value()
            property_to_update.bathrooms = form['bathrooms'].value()
            property_to_update.year_built = form['year_built'].value()
            property_to_update.price = form['price'].value()
            description_to_update.description = form['description'].value()
            property_to_update.save()
            description_to_update.save()
            return redirect('property_details', id=id)
    else:
        property_to_update = Properties.objects.get(pk=id)
        description_to_update = get_object_or_404(Description, property_id=id)
        form = PropertiesUpdateForm(initial={'address': property_to_update.address,
                                             'zip': property_to_update.zip,
                                             'category': property_to_update.category,
                                             'size': property_to_update.size,
                                             'rooms': property_to_update.rooms,
                                             'bathrooms': property_to_update.bathrooms,
                                             'year_built': property_to_update.year_built,
                                             'price': property_to_update.price,
                                             'description': description_to_update.description})
    return render(request, 'Properties/update_property.html', {
        'form': form,
        'prop_id': id
    })


@login_required
def update_property_images(request, id):
    return render(request, 'Properties/property_details_edit_images.html', {
        'Property_images': PropertyImages.objects.filter(property_id=id),
        'prop_id': id
    })


@login_required
def add_property_image(request, id):
    if request.method == 'POST':
        form = PropertiesImagesForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            properties = Properties.objects.get(pk=form['property'].value())
            files = request.FILES.getlist('image')
            for f in files:
                img = default_storage.save('static/images/properties/' + f.name, f.file)
                image = PropertyImages(property=properties, image=img)
                image.save()
            return redirect(update_property_images, id)
    else:
        form = PropertiesImagesForm(initial={'property': id})
    return render(request, 'Properties/upload_property_images.html', {
        'form': form,
        'prop_id': id
    })


@login_required
def delete_property_image(request, id):
    image_to_delete = get_object_or_404(PropertyImages, id=id)
    redirect_location_id = image_to_delete.property_id
    image_to_delete.delete()
    return redirect(update_property_images, redirect_location_id)


def get_property_by_id(request, id):
    prop = get_object_or_404(Properties, id=id)
    prop_seller_user_id = get_object_or_404(PropertySellers, property_id=prop.id).user_id
    if prop.deleted:
        return redirect('all_properties')
    users_prop_list = []
    for i in PropertySellers.objects.filter(user_id=request.user.id):
        users_prop_list.append(i.property_id)

    # ef það er búið að heimsækja síðuna þá er nýjasta vikan sótt
    property_visit = PropertyVisits.objects.filter(property_id=id).order_by('-id').first()
    # ef hún var heimsótt í þessari viku þá er counterinn uppfærður annars er þetta önnur vika og
    # hún er búin til með counter = 1
    if property_visit and property_visit.date.strftime('%W') == datetime.now().strftime('%W') and \
            property_visit.date.strftime('%Y') == datetime.now().strftime('%Y'):
        property_visit.counter = property_visit.counter + 1
        property_visit.save()
    else:
        property_visit = PropertyVisits(property_id=id, counter=1)
        property_visit.save()
    return render(request, 'Properties/property_details.html',
                  {'Property': prop,
                   'UsersProperties': users_prop_list,
                   # listi yfir eignir í körfu notanda búinn til
                   'Cart': [c.property for c in CartItems.objects.filter(user=request.user.id)],
                   # listi yfir eiginir í uppáhaldi hjá notanda búinn til
                   'Favourites': [f.property for f in Favourites.objects.filter(user=request.user.id)],
                   # heildar fjöldi yfir heimsóknir eignar búinn til
                   'PropertyVisits': PropertyVisits.objects.filter(property_id=id).aggregate(count=Sum('counter')),
                   'propertySellerUserId': prop_seller_user_id,
                   'currentUserId': request.user.id
                   })


def get_all_properties(request):
    searches = []
    cart = []
    # ef notandi er skráður inn þá er leitar saga hanns send með
    if request.user.is_authenticated:
        searches = [s.search for s in SearchHistory.objects.filter(user=request.user).order_by('-id')]
        cart = [c.property for c in CartItems.objects.filter(user=request.user.id)]
    props = Properties.objects.filter(deleted=False).order_by('-id')
    paginator = Paginator(props, 9)
    page = request.GET.get('page')
    try:
        display_props = paginator.page(page)
    except PageNotAnInteger:
        display_props = paginator.page(1)
    except EmptyPage:
        display_props = paginator.page(paginator.num_pages)
    context = {'Categories': Categories.objects.all(),
               'Zip': Zip.objects.all(),
               'Cart': cart,
               'Searches': searches,
               'DisplayProps': display_props
               }
    return render(request, 'Properties/index.html', context)


def get_open_houses(request):
    context = {'open_houses': OpenHouses.objects.all()}
    return render(request, 'Properties/open_houses.html', context)


@login_required
def add_open_houses(request):
    if request.method == 'POST':
        form = OpenHousesCreateForm(request=request, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('open_houses')
    else:
        form = OpenHousesCreateForm(initial={'user': request.user}, request=request)
    return render(request, 'Properties/add_open_houses.html', {
        'form': form
    })


def search(request):
    query = request.GET
    props = Properties.objects.filter(deleted=False).order_by('address')
    if query.get('q'):
        props = Properties.objects.filter(Q(deleted=False), Q(address__icontains=query.get('q')))
        SearchHistory.objects.create(user=request.user, search=query.get('q'))
    paginator = Paginator(props, 9)
    page = request.GET.get('page')
    try:
        display_props = paginator.page(page)
    except PageNotAnInteger:
        display_props = paginator.page(1)
    except EmptyPage:
        display_props = paginator.page(paginator.num_pages)

    return render(request, 'Properties/index.html', {'query': query, 'DisplayProps': display_props,
                                                     'Categories': Categories.objects.all(),
                                                     'Zip': Zip.objects.all(),
                                                     'Cart': [c.property for c in
                                                              CartItems.objects.filter(user=request.user.id)],
                                                     'Searches': [s.search for s in SearchHistory.objects.filter(
                                                                  user=request.user).order_by('-id')]
                                                     })


def property_filter(request):
    query = request.GET
    props = Properties.objects.filter(deleted=False)
    if query.get('category'):  # check categories
        props = Properties.objects.filter(Q(deleted=False), Q(category=query.get('category')))
        logger.error(query.get('category'))
        category_query = query.get('category')
    else:
        category_query = ""

    if query.get('zipcodes'):  # check zipcodes
        tmp = Properties.objects.filter(Q(deleted=False), Q(zip=query.get('zipcodes')))
        props = tmp.intersection(props)
        zip_query = query.get('zipcodes')
    else:
        zip_query = ""

    if query.get('roomsfrom'):  # check min rooms
        tmp = Properties.objects.filter(Q(deleted=False), Q(rooms__gte=query.get('roomsfrom')))
        props = tmp.intersection(props)
        roomsfrom_query = query.get('roomsfrom')
    else:
        roomsfrom_query = ""

    if query.get('roomsto') and '+' not in query.get('roomsto'):
        tmp = Properties.objects.filter(Q(deleted=False), Q(rooms__lte=query.get('roomsto')))
        props = tmp.intersection(props)
        roomsto_query = query.get('roomsto')
    else:
        roomsto_query = ""

    if query.get('sizefrom'):
        tmp = Properties.objects.filter(Q(deleted=False), Q(size__gte=query.get('sizefrom')))
        props = tmp.intersection(props)
        sizefrom_query = query.get('sizefrom')
    else:
        sizefrom_query = ""

    if query.get('sizeto') and '+' not in query.get('sizeto'):
        tmp = Properties.objects.filter(Q(deleted=False), Q(size__lte=query.get('sizeto')))
        props = tmp.intersection(props)
        sizeto_query = query.get('sizeto')
    else:
        sizeto_query = ""

    if query.get('pricefrom'):
        tmp = Properties.objects.filter(Q(deleted=False), Q(price__gte=int(query.get('pricefrom')) * 1000000))
        props = tmp.intersection(props)
        pricefrom_query = query.get('pricefrom')
    else:
        pricefrom_query = ""

    if query.get('priceto') and '+' not in query.get('priceto'):
        tmp = Properties.objects.filter(Q(deleted=False), Q(price__lte=int(query.get('priceto')) * 1000000))
        props = tmp.intersection(props)
        priceto_query = query.get('priceto')
    else:
        priceto_query = ""

    if query.get('orderinfo') == 'newestfirst':
        order_query = 'newestfirst'
        props = props.order_by('-id')
    elif query.get('orderinfo') == 'oldestfirst':
        order_query = 'oldestfirst'
        props = props.order_by('id')
    elif query.get('orderinfo') == 'priceascending':
        order_query = 'priceascending'
        props = props.order_by('price')
    elif query.get('orderinfo') == 'pricedescending':
        order_query = 'pricedescending'
        props = props.order_by('-price')
    elif query.get('orderinfo') == 'nameascending':
        order_query = 'nameascending'
        props = props.order_by('address')
    elif query.get('orderinfo') == 'namedescending':
        order_query = 'namedescending'
        props = props.order_by('-address')
    else:
        order_query = 'newestfirst'
        props = props.order_by('-id')

    paginator = Paginator(props, 9)
    page = request.GET.get('page')
    try:
        display_props = paginator.page(page)
    except PageNotAnInteger:
        display_props = paginator.page(1)
    except EmptyPage:
        display_props = paginator.page(paginator.num_pages)

    if request.user in User.objects.all():
        searches = [s.search for s in SearchHistory.objects.filter(
            user=request.user).order_by('-id')]
    else:
        searches = None

    return render(request, 'Properties/index.html', {'DisplayProps': display_props,
                                                     'Categories': Categories.objects.all(),
                                                     'Zip': Zip.objects.all(),
                                                     'Cart': [c.property for c in
                                                              CartItems.objects.filter(user=request.user.id)],
                                                     'Searches': searches,
                                                     'OrderInfo': order_query,
                                                     'CategoryInfo': category_query,
                                                     'ZipInfo': zip_query,
                                                     'RoomsfromInfo': roomsfrom_query,
                                                     'RoomstoInfo': roomsto_query,
                                                     'SizefromInfo': sizefrom_query,
                                                     'SizetoInfo': sizeto_query,
                                                     'PricefromInfo': pricefrom_query,
                                                     'PricetoInfo': priceto_query,
                                                     })


@login_required
def delete_property(request, id):
    properties = get_object_or_404(Properties, pk=id)
    for i in CartItems.objects.filter(property_id=id):
        i.delete()
    properties.deleted = True
    properties.save()
    selling = get_object_or_404(PropertySellers, property_id=id)
    selling.delete()
    if urlparse(request.META.get('HTTP_REFERER')).path == '/users/profile':
        return redirect('profile')
    return redirect('all_properties')


@login_required
def delete_purchased_properties(request):
    # þegar notandi klárar kaup þá er karfan tæmd og eignin merkt ´eytt
    for i in CartItems.objects.filter(user_id=request.user.id):
        i.property.deleted = True
        i.property.save()
    items = CartItems.objects.filter(user=request.user)
    for item in items:
        item.delete()
    # korta upplýsingar ekki geymdar lengur en þarf
    for i in Cards.objects.filter(user_id=request.user.id):
        i.delete()
    return redirect('home')


@login_required
def receipt(request):
    # slembi takkinn finnur eign af handahófi
    random_id = random.choice([p.id for p in Properties.objects.all()])
    item = Properties.objects.filter(id=random_id).first()
    img = PropertyImages.objects.filter(property_id=random_id).first()
    item.deleted = True
    item.save()
    info = {'property': item,
            'img': img}
    return render(request, 'Properties/receipt.html', info)


@login_required
def add_data_from_web(request):
    clearFiles()
    writeToCsv()
    zips = readFromCsv('properties/csv/zip.csv')
    descriptions = readFromCsv('properties/csv/description.csv')
    props = readFromCsv('properties/csv/properties.csv')
    categories = readFromCsv('properties/csv/categories.csv')
    imgs = readFromCsv('properties/csv/propertyImgs.csv')
    print(imgs)
    for i in range(len(props)):
        _zip, created = Zip.objects.get_or_create(zip=str(zips[i][0]),
                                                  city=str(zips[i][1]))
        category, created = Categories.objects.get_or_create(category=str(categories[i][0]))
        prop, created = Properties.objects.get_or_create(address=str(props[i][0]),
                                                         zip_id=_zip.id,
                                                         category_id=category.id,
                                                         size=props[i][1],
                                                         rooms=props[i][2],
                                                         bathrooms=props[i][3],
                                                         year_built=props[i][4],
                                                         price=props[i][5])
        Description.objects.get_or_create(property=prop,
                                          description=descriptions[i][0])
        PropertySellers.objects.get_or_create(property_id=prop.id, user_id=request.user.id)
        image_counter = 1
        while image_counter != 6:
            filename = 'static/images/properties/' + str(props[i][5]) + '_mynd_' + str(image_counter) + '.jpg'
            urllib.request.urlretrieve(imgs[i+image_counter][1], filename)
            PropertyImages.objects.get_or_create(property=prop,
                                                 image=filename)
            image_counter += 1

    return redirect('all_properties')
