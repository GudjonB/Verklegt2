from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_properties, name="allProperties"),
    path('<int:id>', views.get_property_by_id, name="propertyDetails"),
    path('openHouses', views.get_open_houses, name="openHouses"),

    path('create', views.create_properties, name="createProperties"),
    path('upload', views.upload_properties_images, name="uploadPropertyImages"),
    path('addOpenHouses', views.add_open_houses, name="add_open_house"),

    path('delete/<int:id>', views.delete_property, name='deleteProperty'),
    path('update/<int:id>', views.update_property, name='update_property'),

    path('search', views.search, name="search"),
    path('filter', views.filter, name="filter"),

    path('addCartItem/<int:id>', views.add_to_cart, name='addCartItem'),
    path('removeCartItem/<int:id>', views.remove_from_cart, name='removeCartItem'),
    path('data/mbl', views.add_data_from_web, name='addDataFromWeb')
]
