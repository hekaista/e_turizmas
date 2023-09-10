from django.apps import AppConfig


class EgidasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'egidas'

    def ready(self):
        from .signals import create_profile
