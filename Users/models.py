from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from Properties.models import Properties, Zip
from creditcards.models import CardExpiryField


class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70,
                            validators=[RegexValidator(u'^[a-zA-ZáðéíóúýþæöÁÐÉÍÓÚÝÞÆÖ ]*$',
                                                       'Name must only contain alphabetic characters')])
    address = models.CharField(max_length=50,
                               validators=[RegexValidator(u'^[0-9a-zA-ZáðéíóúýþæöÁÐÉÍÓÚÝÞÆÖ -]*$',
                                                          'Invalid character in address')])
    zipCode = models.ForeignKey(Zip, on_delete=models.CASCADE, null=True, blank=True, verbose_name=u"Zip:")
    social = models.CharField(max_length=10, verbose_name=u"Social Security Number:",
                              validators=[RegexValidator(u'^\d{10}$',
                                                         'Social security number must be 10 digits long '
                                                         'and must only contain numbers')])
    image = models.ImageField(upload_to='static/images/users/', verbose_name=u"Profile image:",
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
                            validators=[RegexValidator(u'^[a-zA-ZáðéíóúýþæöÁÐÉÍÓÚÝÞÆÖ ]*$',
                                                       'Name must only contain alphabetic characters')])
    mobile = models.CharField(max_length=7,
                              validators=[RegexValidator(u'^\d{7}$',
                                                         'Mobile must be 7 digits long and must only contain numbers')])
    street_name = models.CharField(max_length=50,
                                   validators=[RegexValidator(u'^[a-zA-ZáðéíóúýþæöÁÐÉÍÓÚÝÞÆÖ ]*$',
                                                              'Street name must only contain alphabetic characters')])
    house_number = models.CharField(max_length=7,
                                    validators=[RegexValidator(u'^[0-9a-zA-Z]*$',
                                                               'Invalid character in house number')])
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default='Iceland')
    city = models.CharField(max_length=50,
                            validators=[RegexValidator(u'^[a-zA-ZáðéíóúýþæöÁÐÉÍÓÚÝÞÆÖ ]*$',
                                                       'City must only contain alphabetic characters')])
    zipCode = models.CharField(max_length=3, verbose_name=u"Zip:",
                               validators=[RegexValidator(u'^\d{3}$',
                                                          'Zip must only contain numbers')])
    social = models.CharField(max_length=10, verbose_name=u"Social Security Number:",
                              validators=[RegexValidator(u'^\d{10}$',
                                                         'Social security number must be 10 digits long '
                                                         'and must only contain numbers')])
    feeling_lucky = models.BooleanField(default=False)


class Cards(models.Model):
    name = models.CharField(max_length=70,
                            validators=[RegexValidator(u'^[a-zA-ZáðéíóúýþæöÁÐÉÍÓÚÝÞÆÖ ]*$',
                                                       'Name must only contain alphabetic characters')]
                            )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    number = models.CharField(max_length=16, verbose_name=u"Credit Card Number:",
                              validators=[RegexValidator(u'^\d{16}$',
                                                         'Credit card number must be 16 characters long and '
                                                         'must only contain numbers')])
    cvc = models.CharField(max_length=3, verbose_name=u"CVC:",
                           validators=[RegexValidator(u'^\d{3}$',
                                                      'CVC must be 3 characters long and must only contain numbers')]
                           )
    expiration = CardExpiryField('expiration date')
