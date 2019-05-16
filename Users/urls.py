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
    path('sellerprofile/<int:id>', views.profile_seller, name='profile_seller'),
    path('staff', views.staff, name='staff'),
    path('profileup', views.update_profile, name='update_profile'),
    path('favourites', views.favourites, name='favourites'),
    path('addFavourite/<int:id>', views.add_to_favourite, name='add_favourite'),
    path('removeFavourite/<int:id>', views.remove_from_favourites, name='remove_favourite'),
    path('removeFavouriteInProfile/<int:id>', views.remove_from_favorites_profile, name='remove_favourite_profile'),


    path('cart', views.cart, name='cart'),
    path('addCartItem/<int:id>', views.add_to_cart, name='add_cart_item'),
    path('removeCartItem/<int:id>', views.remove_from_cart, name='remove_cart_item'),
    path('emptyCart', views.empty_cart, name='empty_cart'),
    path('emptyCartPurchase', views.empty_cart_purchased, name='empty_cart_purchase'),

    path('checkout', views.proceed_to_checkout, name='checkout'),
    path('checkoutCardInfo', views.card_info_checkout, name='checkout_card_info'),
    path('checkoutReadOnly', views.read_only_checkout, name='checkout_readOnly'),
    path('checkoutConfirmation', views.confirmation_checkout, name='checkout_confirmation'),
    path('emptyCheckoutCancel', views.empty_checkout_cancel, name='empty_checkout_cancel'),

    path('add_staff', views.add_staff, name="add_staff"),
    path('about_us', views.about_us, name="about_us")
]

handler404 = 'Users.views.error_404_view'
handler500 = 'Users.views.error_500_view'
