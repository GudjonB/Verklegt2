# Generated by Django 2.2.1 on 2019-05-16 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0017_checkoutinfo_feeling_lucky'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutinfo',
            name='zipCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Properties.Zip', verbose_name='Zip:'),
        ),
    ]