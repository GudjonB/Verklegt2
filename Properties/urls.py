from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_properties, name="allProperties"),
    path('create', views.create_properties, name="createProperties"),
    path('<int:id>', views.get_property_by_id, name="propertyDetails"),
    path('upload', views.upload_properties_images, name="uploadPropertyImages"),
    path('openHouses', views.get_open_houses, name="openHouses"),
    path('addOpenHouses', views.add_open_houses, name="add_open_house"),
    path('filter', views.filter, name="filter"),
    path('search', views.search, name="search"),
    path('delete/<int:id>', views.delete_property, name='deleteProperty'),
    path('addCartItem/<int:id>', views.add_to_cart, name='addCartItem'),
    path('removeCartItem/<int:id>', views.remove_from_cart, name='removeCartItem')
]
