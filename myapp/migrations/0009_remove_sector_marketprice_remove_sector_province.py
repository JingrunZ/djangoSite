# Generated by Django 4.0.6 on 2022-07-23 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_sector_sector_unique_ind'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sector',
            name='marketPrice',
        ),
        migrations.RemoveField(
            model_name='sector',
            name='province',
        ),
    ]
