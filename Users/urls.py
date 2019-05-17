from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('register', views.register, name='register'),
    path('login', LoginView.as_view(template_name='Users/login.html'), name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),

    path('profile', views.profile, name='profile'),
    path('cart', views.cart, name='cart'),
    path('seller_profile/<int:id>', views.profile_seller, name='profile_seller'),
    path('staff', views.staff, name='staff'),
    path('profileup', views.update_profile, name='update_profile'),
    path('favourites', views.favourites, name='favourites'),
    path('add_favourite/<int:id>', views.add_to_favourite, name='add_favourite'),
    path('remove_favourite/<int:id>', views.remove_from_favourites, name='remove_favourite'),

    path('cart', views.cart, name='cart'),
    path('add_cart_item/<int:id>', views.add_to_cart, name='add_cart_item'),
    path('remove_cart_item/<int:id>', views.remove_from_cart, name='remove_cart_item'),
    path('empty_Cart', views.empty_cart, name='empty_cart'),
    path('empty_cart_purchase', views.empty_cart_purchased, name='empty_cart_purchase'),

    path('checkout', views.proceed_to_checkout, name='checkout'),
    path('checkout_card_info', views.card_info_checkout, name='checkout_card_info'),
    path('checkout_read_only', views.read_only_checkout, name='checkout_read_only'),
    path('checkout_confirmation', views.confirmation_checkout, name='checkout_confirmation'),
    path('empty_checkout_cancel', views.empty_checkout_cancel, name='empty_checkout_cancel'),

    path('add_staff', views.add_staff, name="add_staff"),
    path('about_us', views.about_us, name="about_us")
]

handler404 = 'Users.views.error_404_view'
handler500 = 'Users.views.error_500_view'
