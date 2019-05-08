
from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllProperties, name="allproPerties"),
    path('create', views.createProperties, name="createProperties"),
    path('<int:id>', views.getPropertyById, name="propertyDetails")
]