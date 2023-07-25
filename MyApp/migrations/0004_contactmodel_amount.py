# Generated by Django 4.2.2 on 2023-07-22 06:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0003_contactmodel_bankname_contactmodel_cc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmodel',
            name='amount',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)]),
        ),
    ]
