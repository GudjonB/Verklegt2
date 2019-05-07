from django.db import models
from django.contrib.auth.models import User
# from Users.models import Users
# import datetime


class Categories(models.Model):
    category = models.CharField(max_length=255)


class Zip(models.Model):
    zip = models.CharField(max_length=18)
    city = models.CharField(max_length=189)


class Properties(models.Model):
    address = models.CharField(max_length=255)
    zip = models.ForeignKey(Zip, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    size = models.IntegerField()  # max?
    rooms = models.IntegerField()  # max?
    bathrooms = models.IntegerField()  # min? max?
    year_built = models.DateTimeField()  # min=1, max=datetime.date.today().year)
    price = models.FloatField()


class Description(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    description = models.CharField(max_length=999, blank=True)


class OpenHouses(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True)
    length = models.IntegerField()  # Minutes


class PropertyImages(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    images = models.CharField(max_length=999, blank=True)


class PropertyVisits(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    week_number = models.IntegerField()
    counter = models.IntegerField()
