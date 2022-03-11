from django.db import models


class Route(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название маршрута')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Общее время пути')
    from_city = models.ForeignKey('cities.City', on_delete=models.CASCADE, verbose_name='Откуда',
                                  related_name='route_from_sity_set')
    to_city = models.ForeignKey('cities.City', on_delete=models.CASCADE, verbose_name='Куда',
                                  related_name='route_to_sity_set')
    trains = models.ManyToManyField('trains.Train', related_name='routes_set', verbose_name='Список поездов')

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['travel_time']

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('trains:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

