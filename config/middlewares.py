import threading

# Thread local storage - her thread için ayrı bir `user` bilgisi saklanır
_user = threading.local()

# Görünüm dışındaki yerlerde mevcut kullanıcıyı almak için kullanılan fonksiyon
def get_current_user():
    # `_user` thread-local değişkeninden kullanıcıyı döndürür, kullanıcı yoksa `None` döner
    return getattr(_user, 'user', None)


class CurrentUserMiddleware:
    """Her istekte mevcut kullanıcıyı bir thread-local değişkene kaydetmek için kullanılan middleware."""

    # Middleware başlatılırken çağrılan metod
    def __init__(self, get_response):
        self.get_response = get_response  # Bir sonraki middleware veya view'i çağırır

    # Her istekte çağrılan metod
    def __call__(self, request):
        # Eğer kullanıcı giriş yapmışsa, kullanıcıyı thread-local değişkenine kaydeder
        _user.user = request.user if request.user.is_authenticated else None
        # İstek işlenir ve yanıt alınır
        response = self.get_response(request)

        # Yanıt gönderildikten sonra kullanıcı bilgisini temizler
        _user.user = None
        return response
