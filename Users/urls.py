
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="users-index"),
    path('register', views.register, name='register')
]