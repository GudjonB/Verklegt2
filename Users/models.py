from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
import datetime
from django.db import models
from django.contrib.auth.models import User
from Properties.models import Properties, Zip


# Create your models here.


class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,
                            validators=[RegexValidator(r'^[0-9a-zA-Z]*$',
                                                       'Only alphanumeric characters are allowed.',
                                                       'invalid name')])
    address = models.CharField(max_length=255,
                               validators=[RegexValidator(r'^[0-9a-zA-Z]*$',
                                                          'Only alphanumeric characters are allowed.',
                                                          'invalid_address')])
    zipCode = models.ForeignKey(Zip, on_delete=models.CASCADE, null=True, blank=True)
    social = models.CharField(max_length=10,
                              validators=[RegexValidator(r'^[0-9]*$',
                                                         'Only numeric characters are allowed.',
                                                         'invalid_social')])
    image = models.ImageField(upload_to='static/images/users/',
                              default='static/images/users/little-robin-hood-boys-costume.jpg')

    def image_name(self):
        return '/' + self.image.name


class Cards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=16,
                              validators=[RegexValidator(r'^[0-9]*$',
                                                         'Only numeric characters are allowed.',
                                                         'invalid_card_number')])
    cvc = models.CharField(max_length=3,
                           validators=[RegexValidator(r'^[0-9]*$',
                                                      'Only numeric characters are allowed.',
                                                      'invalid_cvc')]
                           )
    expiration = models.CharField(max_length=4)  # TODO: MM/YY
    name = models.CharField(max_length=255,
                            validators=[RegexValidator(r'^[a-zA-Z]*$',
                                                       'Only alphabetic characters are allowed.',
                                                       'invalid_name')]
                            )


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

