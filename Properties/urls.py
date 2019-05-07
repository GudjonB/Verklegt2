
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="properties-index"),
    path('<int:id>', views.getPropertyById, name="propertyDetails"),
    path('createProperty', views.createProperty, name="createProperty")
]