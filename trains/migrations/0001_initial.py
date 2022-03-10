# Generated by Django 4.0.3 on 2022-03-10 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities', '0002_alter_city_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название поезда')),
                ('travel_time', models.PositiveSmallIntegerField(verbose_name='Время в пути')),
                ('from_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_sity_set', to='cities.city', verbose_name='Откуда')),
                ('to_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_sity_set', to='cities.city', verbose_name='Куда')),
            ],
            options={
                'verbose_name': 'Поезд',
                'verbose_name_plural': 'Поезда',
                'ordering': ['from_city'],
            },
        ),
    ]
