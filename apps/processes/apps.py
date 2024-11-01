from django.apps import AppConfig


class ProcessesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.processes'
    label = 'processes'

    def ready(self):
        import apps.processes.signals
