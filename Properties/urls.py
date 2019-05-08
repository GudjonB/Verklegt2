
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="properties-index"),
    path('create', views.createProperties, name="createProperties"),
    path('<int:id>', views.getPropertyById, name="propertyDetails"),
    path('upload', views.propertiesImagesUpload, name="propertyImages")
]