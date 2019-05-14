# Generated by Django 2.2.1 on 2019-05-14 19:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0014_auto_20190514_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cards',
            name='name',
            field=models.CharField(max_length=70, validators=[django.core.validators.RegexValidator('^[a-zA-Záðéíóúýþæö ]*$', 'Name must only contain alphabetic characters')]),
        ),
        migrations.AlterField(
            model_name='checkoutinfo',
            name='city',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Záðéíóúýþæö ]*$', 'City must only contain alphabetic characters')]),
        ),
        migrations.AlterField(
            model_name='checkoutinfo',
            name='house_number',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Invalid character in house number')]),
        ),
        migrations.AlterField(
            model_name='checkoutinfo',
            name='name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Záðéíóúýþæö ]*$', 'Name must only contain alphabetic characters')]),
        ),
        migrations.AlterField(
            model_name='checkoutinfo',
            name='street_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Záðéíóúýþæö ]*$', 'Street name must only contain alphabetic characters')]),
        ),
        migrations.AlterField(
            model_name='checkoutinfo',
            name='zipCode',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Zip must only contain numbers')]),
        ),
        migrations.AlterField(
            model_name='country',
            name='country',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('[a-zA-Z0-9 -]+$', 'Invalid country name')]),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='address',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Záðéíóúýþæö -]*$', 'Invalid character in address')]),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='name',
            field=models.CharField(max_length=70, validators=[django.core.validators.RegexValidator('^[a-zA-Záðéíóúýþæö ]*$', 'Name must only contain alphabetic characters')]),
        ),
        migrations.AlterField(
            model_name='searchhistory',
            name='search',
            field=models.CharField(max_length=50),
        ),
    ]
