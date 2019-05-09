
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_properties, name="allProperties"),
    path('create', views.create_properties, name="createProperties"),
    path('<int:id>', views.get_property_by_id, name="propertyDetails"),
    path('upload', views.upload_properties_images, name="uploadPropertyImages"),
    path('openHouses', views.get_open_houses, name="openHouses")
  #  path('delete/<int:id>', views.delete_property,name='deleteProperty')

]
