# Generated by Django 4.0.6 on 2022-07-22 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_wealth_name'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='wealth',
            constraint=models.UniqueConstraint(fields=('name', 'date'), name='unique_booking'),
        ),
    ]
