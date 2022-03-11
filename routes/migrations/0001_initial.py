# Generated by Django 4.0.3 on 2022-03-10 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities', '0002_alter_city_options'),
        ('trains', '0002_alter_train_travel_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название маршрута')),
                ('travel_times', models.PositiveSmallIntegerField(verbose_name='Общее время пути')),
                ('from_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_from_sity_set', to='cities.city', verbose_name='Откуда')),
                ('to_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_to_sity_set', to='cities.city', verbose_name='Куда')),
                ('trains', models.ManyToManyField(related_name='routes_set', to='trains.train', verbose_name='Список поездов')),
            ],
            options={
                'verbose_name': 'Маршрут',
                'verbose_name_plural': 'Маршруты',
                'ordering': ['travel_times'],
            },
        ),
    ]