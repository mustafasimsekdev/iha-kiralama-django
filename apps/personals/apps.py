from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.personals'
    label = 'personals'

    def ready(self):
        # Uygulama başlatıldığında çalışacak kodları tanımlar.
        # Signals (sinyal) mekanizmasını yükler.

        import apps.personals.signals
        # Bu, uygulama başlatıldığında sinyallerin çalışması için gerekli olan bağlantıları kurar.
