# Generated by Django 4.0.3 on 2022-03-10 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trains', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='train',
            name='travel_time',
            field=models.PositiveSmallIntegerField(verbose_name='Время пути'),
        ),
    ]
