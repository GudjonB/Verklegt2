from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from Properties.forms.properties_form import PropertiesCreateForm
from Properties.forms.open_houses_form import OpenHousesCreateForm
from Properties.forms.properties_images_form import PropertiesImagesForm
from Properties.models import Properties, Description, OpenHouses, Categories, Zip, PropertySellers
import logging
logger = logging.getLogger(__name__)
# logger.error(form['address'].value())


def index(request):
    return render(request, 'Properties/index.html')


def create_properties(request):
    if request.method == 'POST':
        form = PropertiesCreateForm(data=request.POST)
        if form.is_valid():
            properties = form.save()
            description = Description(description=request.POST['description'], property=properties)
            description.save()
            logger.error(request.user.id)
            logger.error(properties.id)
            logger.error(form['address'].value())
            sellers = PropertySellers(user_id=request.user.id, property_id=properties.id)
            sellers.save()
            return redirect('allProperties')
    else:
        form = PropertiesCreateForm()
    return render(request, 'Properties/create_properties.html', {
        'form': form
    })


def get_property_by_id(request, id):
    users_prop_list = []
    for i in PropertySellers.objects.filter(user_id=request.user.id):
        users_prop_list.append(i.property_id)
    return render(request, 'Properties/property_details.html', {
        'Properties': get_object_or_404(Properties, pk=id),
        'UsersProperties': users_prop_list
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
               'Zip': Zip.objects.all()
               }
    return render(request, 'Properties/index.html', context)


def get_open_houses(request):
    context = {'OpenHouses' : OpenHouses.objects.all()}
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
                                                      'Zip': Zip.objects.all()
                                                      })

def filter(request):
    query = request.GET
    props = Properties.objects.all().order_by('-id')
    if query.getlist('category'): #check categories
        props = Properties.objects.filter(Q(category__in=query.getlist('category'))).order_by('category').order_by('address')
    if query.get('zipcodes'): #check zipcodes
        tmp = Properties.objects.filter(Q(zip__in=query.get('zipcodes')))
        props = tmp.intersection(props)
    if query.get('roomsfrom'): #check min rooms
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
                                                      'Zip': Zip.objects.all()
                                                     })

  
def delete_property(request, id):
    properties = get_object_or_404(Properties, pk=id)
    properties.deleted = True
    properties.save()
    return redirect('allProperties')

