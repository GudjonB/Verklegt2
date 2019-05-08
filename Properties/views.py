from django.shortcuts import render, redirect, get_object_or_404
from Properties.forms.propertiesForm import PropertiesCreateForm
from Properties.models import Properties, Description


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

  
def getPropertyById(request, id):
    return render(request, 'Properties/propertyDetails.html', {
        'Properties': get_object_or_404(Properties, pk=id)
    })

def getAllProperties(request):
    context =  {'Properties': Properties.objects.all()}
    return render(request, 'Properties/index.html',context )