# Generated by Django 2.2.1 on 2019-05-14 12:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Properties', '0003_auto_20190513_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='category',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[a-zA-Z -]*$', 'Only alphabetic characters are allowed.', 'invalid_category')]),
        ),
        migrations.AlterField(
            model_name='description',
            name='description',
            field=models.CharField(blank=True, max_length=4000, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z ]*$', 'Only alphanumeric characters are allowed.', 'invalid_description')]),
        ),
        migrations.AlterField(
            model_name='properties',
            name='address',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z ]*$', 'Only alphanumeric characters are allowed.', 'invalid_address')]),
        ),
        migrations.AlterField(
            model_name='zip',
            name='city',
            field=models.CharField(max_length=189, validators=[django.core.validators.RegexValidator('^[a-zA-Z ]*$', 'Only alphabetic characters are allowed.', 'invalid_city')]),
        ),
        migrations.AlterField(
            model_name='zip',
            name='zip',
            field=models.CharField(max_length=18, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Only alphanumeric characters are allowed.', 'invalid_zip')]),
        ),
    ]