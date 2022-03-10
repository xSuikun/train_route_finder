from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Train(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название поезда')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Время в пути')
    from_city = models.ForeignKey('cities.City', on_delete=models.CASCADE, verbose_name='Откуда',
                                  related_name='from_sity_set')
    to_city = models.ForeignKey('cities.City', on_delete=models.CASCADE, verbose_name='Куда',
                                  related_name='to_sity_set')

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        ordering = ['from_city']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('trains:detail', kwargs={'pk': self.pk})

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError("Поля 'Откуда' и 'Куда' не могут содержать один и тот же город")
        qs = Train.objects.filter(from_city=self.from_city, to_city=self.to_city,
                                  travel_time=self.travel_time).exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError('Поезд с таким маршрутом и временем пути уже существует')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
