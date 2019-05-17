from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_properties, name="all_properties"),
    path('<int:id>', views.get_property_by_id, name="property_details"),
    path('open_houses', views.get_open_houses, name="open_houses"),
    path('create', views.create_properties, name="create_properties"),
    path('add_open_houses', views.add_open_houses, name="add_open_house"),
    path('delete_open_house/<int:id>', views.delete_open_house, name="delete_open_house"),
    path('delete/<int:id>', views.delete_property, name='delete_property'),
    path('delete_purchased_properties', views.delete_purchased_properties, name='delete_purchased_properties'),
    path('update/<int:id>', views.update_property, name='update_property'),
    path('edit_image/<int:id>', views.update_property_images, name='update_property_images'),
    path('add_image/<int:id>', views.add_property_image, name='add_property_image'),
    path('delete_image/<int:id>', views.delete_property_image, name='delete_property_image'),
    path('search', views.search, name="search"),
    path('filter', views.property_filter, name="filter"),
    path('data/mbl', views.add_data_from_web, name='add_data_from_web'),
    path('receipt', views.receipt, name="receipt")
]
