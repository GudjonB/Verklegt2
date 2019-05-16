# Generated by Django 2.2.1 on 2019-05-16 17:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0018_auto_20190516_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutinfo',
            name='zipCode',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Zip must only contain numbers')], verbose_name='Zip:'),
        ),
    ]