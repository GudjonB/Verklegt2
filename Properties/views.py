from urllib.parse import urlparse

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from Properties.forms.properties_form import PropertiesCreateForm
from Properties.forms.open_houses_form import OpenHousesCreateForm
from Properties.forms.properties_images_form import PropertiesImagesForm
from Properties.models import Properties, Description, OpenHouses, Categories, Zip, PropertySellers, PropertyImages
from Users.models import CartItems, Favourites
from Helpers.getData import clearFiles, writeToCsv, readFromCsv
import logging
import urllib


logger = logging.getLogger(__name__)


# logger.error(form['address'].value())

def index(request):
    return render(request, 'Properties/index.html')


def create_properties(request):
    if request.method == 'POST':
        form = PropertiesCreateForm(request.POST, request.FILES)
        if form.is_valid():
            properties = form.save()
            description = Description(description=request.POST['description'], property=properties)
            description.save()
            sellers = PropertySellers(user_id=request.user.id, property_id=properties.id)
            sellers.save()
            images = PropertyImages(image=form.cleaned_data['image'], property_id=properties.id)
            images.save()
            return redirect('allProperties')
    else:
        form = PropertiesCreateForm()
    return render(request, 'Properties/create_properties.html', {
        'form': form
    })


def create_properties_images(request):
    if request.method == 'POST':
        form = PropertiesImagesForm(data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PropertiesImagesForm()


def update_property(request, id):
    if request.method == 'POST':
        form = PropertiesCreateForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            property_to_update = get_object_or_404(Properties, pk=id)
            description_to_update = get_object_or_404(Description, property_id=id)
            property_image_to_update = get_object_or_404(PropertyImages, property_id=id)

            property_to_update.address = form['address'].value()
            property_to_update.zip_id = form['zip'].value()
            property_to_update.category_id = form['category'].value()
            property_to_update.size = form['size'].value()
            property_to_update.rooms = form['rooms'].value()
            property_to_update.bathrooms = form['bathrooms'].value()
            property_to_update.year_built = form['year_built'].value()
            property_to_update.price = form['price'].value()
            property_image_to_update.image = form['image'].value()
            description_to_update.description = form['description'].value()
            property_to_update.save()
            description_to_update.save()
            property_image_to_update.save()
            return redirect('propertyDetails', id=id)
    else:
        property_to_update = Properties.objects.get(pk=id)
        description_to_update = get_object_or_404(Description, property_id=id)
        property_image_to_update = get_object_or_404(PropertyImages, property_id=id)
        form = PropertiesCreateForm(initial={'address': property_to_update.address,
                                             'zip': property_to_update.zip,
                                             'category': property_to_update.category,
                                             'size': property_to_update.size,
                                             'rooms': property_to_update.rooms,
                                             'bathrooms': property_to_update.bathrooms,
                                             'year_built': property_to_update.year_built,
                                             'price': property_to_update.price,
                                             'image': property_image_to_update.image.name,
                                             'description': description_to_update.description})
    return render(request, 'Properties/update_property.html', {
        'form': form,
        'prop_id': id
    })


def get_property_by_id(request, id):
    users_prop_list = []
    for i in PropertySellers.objects.filter(user_id=request.user.id):
        users_prop_list.append(i.property_id)
    return render(request, 'Properties/property_details.html', {
        'Property': get_object_or_404(Properties, pk=id),
        'UsersProperties': users_prop_list,
        'Cart': [c.property for c in CartItems.objects.filter(user=request.user.id)],
        'Favourites': [f.property for f in Favourites.objects.filter(user=request.user.id)]
    })


def upload_properties_images(request):
    if request.method == 'POST':
        form = PropertiesImagesForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('allProperties')
    else:
        form = PropertiesImagesForm()
    return render(request, 'Properties/upload_property_images.html', {
        'form': form
    })


def get_all_properties(request):
    context = {'Properties': Properties.objects.all().order_by('-id'),
               'Categories': Categories.objects.all(),
               'Zip': Zip.objects.all(),
               'Cart': [c.property for c in CartItems.objects.filter(user=request.user.id)]
               }
    return render(request, 'Properties/index.html', context)


def add_to_cart(request, id):
    item = CartItems(property=get_object_or_404(Properties, pk=id), user=request.user)
    item.save()
    return redirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, id):
    item = CartItems.objects.filter(property_id=id, user=request.user)
    item.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def get_open_houses(request):
    context = {'OpenHouses': OpenHouses.objects.all()}
    return render(request, 'Properties/open_houses.html', context)


'''
def get_new_properties(request):
    context = {'Properties': Properties.objects.all().order_by('-id')[:3]}
    return render(request, 'Users/index.html', context)
'''


def add_open_houses(request):
    if request.method == 'POST':
        form = OpenHousesCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('openHouses')
    else:
        form = OpenHousesCreateForm()
    return render(request, 'Properties/add_open_houses.html', {
        'form': form
    })


def search(request):
    query = request.GET
    props = Properties.objects.all().order_by('address')
    if query.get('q'):
        props = Properties.objects.filter(Q(address__icontains=query.get('q')))
    return render(request, 'Properties/index.html', {'query': query, 'Properties': props,
                                                     'Categories': Categories.objects.all(),
                                                     'Zip': Zip.objects.all(),
                                                     'Cart': [c.property for c in
                                                              CartItems.objects.filter(user=request.user.id)]
                                                     })


def filter(request):
    query = request.GET
    props = Properties.objects.all().order_by('-id')
    if query.getlist('category'):  # check categories
        props = Properties.objects.filter(Q(category__in=query.getlist('category'))).order_by('category').order_by(
            'address')
    if query.get('zipcodes'):  # check zipcodes
        tmp = Properties.objects.filter(Q(zip__in=query.get('zipcodes')))
        props = tmp.intersection(props)
    if query.get('roomsfrom'):  # check min rooms
        tmp = Properties.objects.filter(Q(rooms__gte=query.get('roomsfrom')))
        props = tmp.intersection(props)
    if query.get('roomsto') and '+' not in query.get('roomsto'):
        tmp = Properties.objects.filter(Q(rooms__lte=query.get('roomsto')))
        props = tmp.intersection(props)
    if query.get('sizefrom'):
        tmp = Properties.objects.filter(Q(size__gte=query.get('sizefrom')))
        props = tmp.intersection(props)
    if query.get('sizeto') and '+' not in query.get('sizeto'):
        tmp = Properties.objects.filter(Q(size__lte=query.get('sizeto')))
        props = tmp.intersection(props)
    if query.get('pricefrom'):
        tmp = Properties.objects.filter(Q(price__gte=query.get('pricefrom')))
        props = tmp.intersection(props)
    if query.get('priceto') and '+' not in query.get('priceto'):
        tmp = Properties.objects.filter(Q(price__lte=query.get('priceto')))
        props = tmp.intersection(props)
    if query.get('ordertime') == 'Newest':
        props = props.order_by('-id')
    if query.get('ordertime') == 'Oldest':
        props = props.order_by('id')
    if query.get('orderinfo'):
        if query.get('orderinfo') == 'priceascending':
            props = props.order_by('price')
        elif query.get('orderinfo') == 'pricedescending':
            props = props.order_by('-price')
        elif query.get('orderinfo') == 'nameascending':
            props = props.order_by('-address')
        else:
            props = props.order_by('address')

    return render(request, 'Properties/index.html', {'Properties': props,
                                                     'Categories': Categories.objects.all(),
                                                     'Zip': Zip.objects.all(),
                                                     'Cart': [c.property for c in
                                                              CartItems.objects.filter(user=request.user.id)]
                                                     })


def delete_property(request, id):
    properties = get_object_or_404(Properties, pk=id)
    properties.deleted = True
    properties.save()
    selling = get_object_or_404(PropertySellers, property_id=id)
    selling.delete()
    if urlparse(request.META.get('HTTP_REFERER')).path == '/users/profile':
        return redirect('profile')
    return redirect('allProperties')


def add_data_from_web(request):
    clearFiles()
    writeToCsv()
    zips = readFromCsv('properties/csv/zip.csv')
    descriptions = readFromCsv('properties/csv/description.csv')
    props = readFromCsv('properties/csv/properties.csv')
    categories = readFromCsv('properties/csv/categories.csv')
    imgs = readFromCsv('properties/csv/propertyImgs.csv')
    print(imgs)
    j = 0
    for i in range(len(props)):
        zip, created = Zip.objects.get_or_create(zip=str(zips[i][0]),
                                                 city=str(zips[i][1]))
        category, created = Categories.objects.get_or_create(category=str(categories[i][0]))
        property, created = Properties.objects.get_or_create(address=str(props[i][0]),
                                                             zip_id=zip.id,
                                                             category_id=category.id,
                                                             size=props[i][1],
                                                             rooms=props[i][2],
                                                             bathrooms=props[i][3],
                                                             year_built=props[i][4],
                                                             price=props[i][5])
        Description.objects.get_or_create(property=property,
                                          description=descriptions[i][0])

        imageCounter = 1
        while imageCounter != 4:
            filename = 'static/images/properties/' + str(props[i][5]) + '_mynd_' + str(imageCounter) + '.jpg'
            urllib.request.urlretrieve(imgs[j][1] , filename)
            PropertyImages.objects.get_or_create(property=property,
                                                 image=filename)
            imageCounter += 1
            j += 1

    return redirect('allProperties')
