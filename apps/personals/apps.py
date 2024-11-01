from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.personals'
    label = 'personals'

    def ready(self):
        import apps.personals.signals
