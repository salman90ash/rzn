from django.apps import AppConfig


class RznConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rzn'

    def ready(self):
        from scheduler import updater
        updater.start()
