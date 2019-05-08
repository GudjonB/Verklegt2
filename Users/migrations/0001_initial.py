# Generated by Django 2.2.1 on 2019-05-08 09:21

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Properties', '0002_auto_20190508_0921'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.', 'invalid_address')])),
                ('social', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Only numeric characters are allowed.', 'invalid_social')])),
                ('image', models.CharField(blank=True, max_length=999)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('zipCode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Properties.Zip')),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiration', models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.date(2019, 5, 8))])),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Properties.Properties')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Properties.Properties')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Properties.Properties')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Only numeric characters are allowed.', 'invalid_card_number')])),
                ('cvc', models.CharField(max_length=3, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Only numeric characters are allowed.', 'invalid_cvc')])),
                ('expiration', models.CharField(max_length=4)),
                ('name', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Only alphabetic characters are allowed.', 'invalid_name')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
