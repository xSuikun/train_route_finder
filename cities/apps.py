from django.apps import AppConfig


class CitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cities'
    verbose_name = 'Населенный пункт'
    verbose_name_plural = 'Населенные пункты'
