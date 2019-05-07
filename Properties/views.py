from django.shortcuts import render, get_object_or_404
from Properties.models import Properties

# Create your views here.
def index(request) :
    return render(request, 'Properties/index.html')

def createProperty(request):
    if request.method == 'POST':
        print(1)
    else:
        print(2)

    return render(request, 'properties/createProperty.html', {
        'form': form
    })

def getPropertyById(request, id):
    return render(request, 'Properties/propertyDetails.html', {
        'Properties': get_object_or_404(Properties, pk=id)
    })