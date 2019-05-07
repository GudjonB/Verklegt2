from django.shortcuts import render, redirect
from Properties.forms.propertiesForm import PropertiesCreateForm
from Properties.models import Properties, Description

# Create your views here.


def index(request):
    return render(request, 'Properties/index.html')


def createProperties(request):
    if request.method == 'POST':
        form = PropertiesCreateForm(data=request.POST)
        if form.is_valid():
            properties = form.save()
            description = Description(description=request.POST['description'], property=properties)
            description.save()
            return redirect('properties-index')
    else:
        form = PropertiesCreateForm()
    return render(request, 'Properties/createProperties.html', {
        'form': form
    })
