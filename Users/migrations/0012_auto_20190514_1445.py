# Generated by Django 2.2.1 on 2019-05-14 14:45

import creditcards.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0011_auto_20190514_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cards',
            name='expiration',
            field=creditcards.models.CardExpiryField(verbose_name='expiration date'),
        ),
    ]