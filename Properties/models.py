from django import forms
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
# from Users.models import Users
# import datetime


class Categories(models.Model):
    category = models.CharField(max_length=255,
                                validators=[RegexValidator(r'^[a-zA-Z]*$',
                                                           'Only alphabetic characters are allowed.',
                                                           'invalid_category')])

    def __str__(self):
        return self.category


class Zip(models.Model):
    zip = models.CharField(max_length=18,
                           validators=[RegexValidator(r'^[0-9a-zA-Z]*$',
                                                      'Only alphanumeric characters are allowed.',
                                                      'invalid_zip')])
    city = models.CharField(max_length=189,
                            validators=[RegexValidator(r'^[a-zA-Z]*$',
                                                       'Only alphabetic characters are allowed.',
                                                       'invalid_city')])


class Properties(models.Model):
    address = models.CharField(max_length=255,
                               validators=[RegexValidator(r'^[0-9a-zA-Z]*$',
                                                          'Only alphanumeric characters are allowed.',
                                                          'invalid_address')])
    zip = models.ForeignKey(Zip, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, default=1, on_delete=models.CASCADE)
    size = models.IntegerField()
    rooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    year_built = models.CharField(max_length=4, blank=True, null=True,
                                  validators=[RegexValidator(r'^[0-9]*$',
                                                             'Only numeric characters are allowed.',
                                                             'invalid_year')]
                                  )
    price = models.FloatField(validators=[MinValueValidator(0.0)])

    def __str__(self):
        return self.address


class Description(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    description = models.CharField(max_length=999, blank=True,
                                   validators=[RegexValidator(r'^[0-9a-zA-Z]*$',
                                                              'Only alphanumeric characters are allowed.',
                                                              'invalid_description')])

    def __str__(self):
       return self.description


class OpenHouses(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True)
    length = models.PositiveIntegerField(blank=True)  # Minutes


class PropertyImages(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/images/properties/')

    def __str__(self):
        return self.image.name


class PropertyVisits(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    week_number = models.PositiveIntegerField(blank=True)
    counter = models.PositiveIntegerField(blank=True)
