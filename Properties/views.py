from django.shortcuts import render, redirect, get_object_or_404
from Properties.forms.properties_form import PropertiesCreateForm
from Properties.forms.properties_images_form import PropertiesImagesForm
from Properties.models import Properties, Description, OpenHouses, Categories, Zip


def index(request):
    return render(request, 'Properties/index.html')


def create_properties(request):
    if request.method == 'POST':
        form = PropertiesCreateForm(data=request.POST)
        if form.is_valid():
            properties = form.save()
            description = Description(description=request.POST['description'], property=properties)
            description.save()
            return redirect('allProperties')
    else:
        form = PropertiesCreateForm()
    return render(request, 'Properties/create_properties.html', {
        'form': form
    })

  
def get_property_by_id(request, id):
    return render(request, 'Properties/property_details.html', {
        'Properties': get_object_or_404(Properties, pk=id)
    })


def upload_properties_images(request):
    if request.method == 'POST':
        form = PropertiesImagesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('allProperties')
    else:
        form = PropertiesImagesForm()
    return render(request, 'Properties/upload_property_images.html', {
        'form': form
    })

  
def get_all_properties(request):
    context = {'Properties': Properties.objects.all(),
               'Categories': Categories.objects.all(),
               'Zip': Zip.objects.all()
              }
    return render(request, 'Properties/index.html', context)


def get_open_houses(request):
    context = {'OpenHouses' : OpenHouses.objects.all()}
    return render(request, 'Properties/open_houses.html', context)


def get_new_properties(request):
    context = {'Properties': Properties.objects.all().order_by('-id')}
    return render(request, 'users/index.html', context)
