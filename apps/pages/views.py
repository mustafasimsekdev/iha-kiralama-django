from django.views.generic import TemplateView
from config import TemplateLayout

class PagesView(TemplateView):
    # `TemplateView` sınıfını temel alan bir görünüm sınıfı oluşturur.

    # Görünüme ait bağlam verilerini (context data) elde eden özel bir işlev.
    def get_context_data(self, **kwargs):
        # Üst sınıfın `get_context_data` işlevini çağırarak varsayılan bağlam verilerini alır.
        # `TemplateLayout.init` fonksiyonunu kullanarak global düzen (layout) ayarlarını başlatır.
        # Bu başlatma işlemi, bağlamı daha kapsamlı hale getirir.
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Güncellenmiş bağlamı döndürür.
        return context
