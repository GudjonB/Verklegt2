from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="users-index"),
    path('register', views.register, name='register'),
    path('login', LoginView.as_view(template_name='Users/login.html'), name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('profileup', views.update_profile, name='update_profile'),
    path('profile', views.profile, name='profile'),
    path('makeOffers', views.make_offers, name='makeOffers'),
    path('cart', views.cart, name='cart'),
    path('favourites', views.favourites, name='favourites'),
    path('addFavourite/<int:id>', views.add_to_favourite, name='addFavourite'),
    path('removeFavourite/<int:id>', views.remove_from_favourites, name='removeFavourite'),
    path('addCartItem/<int:id>', views.add_to_cart, name='addCartItem'),
    path('removeCartItem/<int:id>', views.remove_from_cart, name='removeCartItem')
]

