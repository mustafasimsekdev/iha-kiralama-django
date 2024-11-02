from django.apps import AppConfig


# Processes uygulaması için özel yapılandırma sınıfı
class ProcessesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.processes'
    label = 'processes'

    # Uygulama başlatıldığında çalışacak işlemleri tanımlar
    def ready(self):
        # Uygulama başlatıldığında `signals` modülünü içe aktarır
        # Bu, `apps/processes/signals.py` dosyasındaki sinyallerin çalışmasını sağlar
        import apps.processes.signals
