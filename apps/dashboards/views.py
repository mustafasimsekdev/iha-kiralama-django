from django.views.generic import TemplateView
from config import TemplateLayout


class DashboardsView(TemplateView):
    # `TemplateView` sınıfını temel alan bir sınıf görünümü oluşturur.

    def get_context_data(self, **kwargs):
        # `super().get_context_data(**kwargs)` ile üst sınıftan varsayılan bağlam verilerini alır.
        # `TemplateLayout.init()` fonksiyonu ile global düzen (layout) ayarlarını başlatır.
        # Bu başlatma işlemi, bağlamı daha düzenli hale getirir.
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Güncellenmiş bağlamı döndürür.
        return context
