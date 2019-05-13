from django.core.validators import RegexValidator
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
                                                          'invalid address')])
    zipCode = models.ForeignKey(Zip, on_delete=models.CASCADE, null=True, blank=True)
    social = models.CharField(max_length=10,
                              validators=[RegexValidator(r'^[0-9]*$',
                                                         'Only numeric characters are allowed.',
                                                         'invalid social')])
    image = models.ImageField(upload_to='static/images/users/',
                              default='static/images/users/little-robin-hood-boys-costume.jpg',
                              blank=True, null=True)

    def image_name(self):
        return '/' + self.image.name


class Country(models.Model):
    country = models.CharField(max_length=155,
                               validators=[RegexValidator(r'^[a-zA-Z]*$',
                                                          'Only alphabetic characters are allowed.',
                                                          'invalid country')])

    def __str__(self):
        return self.country


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

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search = models.CharField(max_length=110)

class CheckoutInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255,
                            validators=[RegexValidator(r'^[0-9a-zA-Z]*$',
                                                       'Only alphanumeric characters are allowed.',
                                                       'invalid name')])
    mobile = models.CharField(max_length=7,
                              validators=[RegexValidator(r'^[0-9]*$',
                                                         'Only numeric characters are allowed.',
                                                         'invalid mobile')])
    street_name = models.CharField(max_length=255,
                                   validators=[RegexValidator(r'^[0-9a-zA-Z]*$',
                                                              'Only alphanumeric characters are allowed.',
                                                              'invalid street name')])
    house_number = models.CharField(max_length=155,
                                    validators=[RegexValidator(r'^[0-9a-zA-Z]*$',
                                                               'Only alphanumeric characters are allowed.',
                                                               'invalid house number')])
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default='Iceland')
    city = models.CharField(max_length=255,
                            validators=[RegexValidator(r'^[a-zA-Z]*$',
                                                       'Only alphabetic characters are allowed.',
                                                       'invalid_name')])
    zipCode = models.CharField(max_length=155,
                               validators=[RegexValidator(r'^[0-9a-zA-Z]*$',
                                                          'Only alphanumeric characters are allowed.',
                                                          'invalid zip')])
    social = models.CharField(max_length=10,
                              validators=[RegexValidator(r'^[0-9]*$',
                                                         'Only numeric characters are allowed.',
                                                         'invalid_social')])


