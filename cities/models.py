from django.db import models
from django.urls import reverse


class City(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название', unique=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cities:detail', kwargs={'pk': self.pk})