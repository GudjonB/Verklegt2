from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from Properties.models import Properties, Zip
from creditcards.models import CardExpiryField

# Create your models here.

class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70,
                            validators=[RegexValidator(u'^[a-zA-Záðéíóúýþæö ]*$',
                                                       'Name must only contain alphabetic characters')])
    address = models.CharField(max_length=50,
                               validators=[RegexValidator(u'^[0-9a-zA-Záðéíóúýþæö -]*$',
                                                          'Invalid character in address')])
    zipCode = models.ForeignKey(Zip, on_delete=models.CASCADE, null=True, blank=True)
    social = models.CharField(max_length=10,
                              validators=[RegexValidator(u'^.{10}[0-9]*$',
                                                         'Social security number must be 10 digits long and must only contain numbers')])
    image = models.ImageField(upload_to='static/images/users/',
                              default='static/images/users/little-robin-hood-boys-costume.jpg',
                              blank=True, null=True)

    def image_name(self):
        return '/' + self.image.name


class Country(models.Model):
    country = models.CharField(max_length=50,
                               validators=[RegexValidator(u'[a-zA-Z0-9 -]+$',
                                                          'Invalid country name')])

    def __str__(self):
        return self.country


class Cards(models.Model):
    name = models.CharField(max_length=70,
                            validators=[RegexValidator(u'^[a-zA-Záðéíóúýþæö ]*$',
                                                       'Name must only contain alphabetic characters')]
                            )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=16,
                              validators=[RegexValidator(u'^.{16}[0-9]*$',
                                                         'Credit card number must be 16 characters long and must only contain numbers')])
    cvc = models.CharField(max_length=3,
                           validators=[RegexValidator(u'^.{3}[0-9]*$',
                                                      'CVC must be 3 characters long and must only contain numbers')]
                           )
    expiration = CardExpiryField('expiration date')



class Offers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    expiration = models.DateTimeField(blank=True)
    amount = models.IntegerField()


class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)


class CartItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search = models.CharField(max_length=50)

class CheckoutInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50,
                            validators=[RegexValidator(u'^[a-zA-Záðéíóúýþæö ]*$',
                                                       'Name must only contain alphabetic characters')])
    mobile = models.CharField(max_length=7,
                              validators=[RegexValidator(u'^.{7}[0-9]*$',
                                                         'Mobile must be 7 digits long and must only contain numbers')])
    street_name = models.CharField(max_length=50,
                                   validators=[RegexValidator(u'^[a-zA-Záðéíóúýþæö ]*$',
                                                              'Street name must only contain alphabetic characters')])
    house_number = models.CharField(max_length=7,
                                    validators=[RegexValidator(u'^[0-9a-zA-Z]*$',
                                                               'Invalid character in house number')])
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default='Iceland')
    city = models.CharField(max_length=50,
                            validators=[RegexValidator(u'^[a-zA-Záðéíóúýþæö ]*$',
                                                       'City must only contain alphabetic characters')])
    zipCode = models.CharField(max_length=5,
                               validators=[RegexValidator(u'^[0-9]*$',
                                                          'Zip must only contain numbers')])
    social = models.CharField(max_length=10,
                              validators=[RegexValidator(u'^.{10}[0-9]*$',
                                                         'Social security number must be 10 digits long and must only contain numbers')])


