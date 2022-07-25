# Generated by Django 4.0.6 on 2022-07-23 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_wealth_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='中文简称')),
                ('industry', models.CharField(max_length=100, verbose_name='行业')),
                ('province', models.CharField(max_length=100, verbose_name='省份')),
                ('marketPrice', models.CharField(max_length=100, verbose_name='市值')),
            ],
        ),
        migrations.AddConstraint(
            model_name='sector',
            constraint=models.UniqueConstraint(fields=('name', 'industry'), name='unique_ind'),
        ),
    ]