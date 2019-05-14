from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="users-index"),
    path('register', views.register, name='register'),
    path('login', LoginView.as_view(template_name='Users/login.html'), name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),


    path('profile', views.profile, name='profile'),
    path('cart', views.cart, name='cart'),
    path('sellerprofile/<int:id>', views.profile_seller, name='profile_seller'),
    path('profileup', views.update_profile, name='update_profile'),
    path('favourites', views.favourites, name='favourites'),
    path('addFavourite/<int:id>', views.add_to_favourite, name='addFavourite'),
    path('removeFavourite/<int:id>', views.remove_from_favourites, name='removeFavourite'),
    path('removeFavouriteInProfile/<int:id>', views.remove_from_favorites_profile, name='removeFavouriteProfile'),


    path('makeOffers', views.make_offers, name='makeOffers'),


    path('cart', views.cart, name='cart'),
    path('addCartItem/<int:id>', views.add_to_cart, name='addCartItem'),
    path('removeCartItem/<int:id>', views.remove_from_cart, name='removeCartItem'),
    path('emptyCart/', views.empty_cart, name='emptyCart'),
    path('emptyCartPurchase', views.empty_cart_purchased, name='emptyCartPurchase'),


    path('checkout', views.proceed_to_checkout, name='checkout'),
    path('checkoutCardInfo', views.card_info_checkout, name='checkoutCardInfo'),
    path('checkoutReadOnly', views.read_only_checkout, name='checkoutReadOnly'),
    path('checkoutConfirmation', views.confirmation_checkout, name='checkoutConfirmation'),
    path('emptyCheckoutCancel', views.empty_checkout_cancel, name='emptyCheckoutCancel'),
    # path('emptyCardInfo', views.empty_card_info, name='emptyCardInfo'),


    path('add_staff', views.add_staff, name="addStaff")
]

handler404 = 'Users.views.error_404_view'
handler500 = 'Users.views.error_500_view'
