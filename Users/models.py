from django.db import models
from django.contrib.auth.models import User
from Properties.models import Properties, Zip
# Create your models here.


class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    zipCode = models.ForeignKey(Zip, on_delete=models.CASCADE)
    social = models.CharField(max_length=10)


class ProfileImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.CharField(max_length=999, blank=True)


class Cards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=16)
    cvc = models.CharField(max_length=3)
    expiration = models.CharField(max_length=4)
    name = models.CharField(max_length=255)


class Offers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    expiration = models.DateTimeField()


class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)


class CartItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
