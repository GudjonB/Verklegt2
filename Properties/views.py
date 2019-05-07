from django.shortcuts import render

# Create your views here.
def index(request) :
    return render(request, 'Properties/index.html')

def createCandy(request):
    if request.method == 'POST':
        print(1)
    else
        print(2)

    return render(request, 'properties/createProperty.html', {
        'form': form
    })