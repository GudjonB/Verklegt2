from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.db import models


def validate_date(value):
    if value.isoformat() < datetime.today().isoformat():
        raise ValidationError("Date cannot be in the past")


class Categories(models.Model):
    category = models.CharField(max_length=30,
                                validators=[RegexValidator(u'^[a-zA-Z -]*$',
                                                           'Category must only contain alphabetic characters')])

    def __str__(self):
        return self.category


class Zip(models.Model):
    zip = models.CharField(max_length=7,
                           validators=[RegexValidator(u'^[0-9]*$',
                                                      'Zip must only contain numbers')])
    city = models.CharField(max_length=50,
                            validators=[RegexValidator(u'^[0-9a-zA-ZáðéíóúýþæöÁÐÉÍÓÚÝÞÆÖ -]*$',
                                                       'Invalid character in address')])

    class Meta:
        ordering = ['zip']

    def __str__(self):
        return self.zip


class Properties(models.Model):
    address = models.CharField(max_length=50,
                               validators=[RegexValidator(u'^[0-9a-zA-ZáðéíóúýþæöÁÐÉÍÓÚÝÞÆÖ -]*$',
                                                          'Invalid character in address')])
    zip = models.ForeignKey(Zip, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, default=1, on_delete=models.CASCADE)
    size = models.FloatField(validators=[MinValueValidator(0.0)])
    rooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    year_built = models.CharField(max_length=4, blank=True, null=True,
                                  validators=[RegexValidator(u'^\d{4}$',
                                                             'Year must be 4 digits long and must only contain numbers')])
    price = models.DecimalField(decimal_places=0, max_digits=15, validators=[MinValueValidator(0)])
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.address


class Description(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    description = models.CharField(max_length=4000, blank=True,
                                   validators=[RegexValidator(u'^[0-9a-zA-ZáðéíóúýþæöÁÐÉÍÓÚÝÞÆÖ -]*$',
                                                              'Invalid character in description')])

    def __str__(self):
        return self.description


class OpenHouses(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True, validators=[validate_date])
    length = models.PositiveIntegerField(blank=True)  # Minutes


class PropertyImages(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/images/properties/')

    def __str__(self):
        return '/' + self.image.name


class PropertyVisits(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    counter = models.PositiveIntegerField(blank=True)


class PropertySellers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
