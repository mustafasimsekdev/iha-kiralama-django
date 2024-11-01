# middlewares.py

import threading

# Thread local storage
_user = threading.local()


def get_current_user():
    """Return the current user outside of views."""
    return getattr(_user, 'user', None)


class CurrentUserMiddleware:
    """Middleware to save current user in a thread-local variable."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Kullanıcıyı thread-local değişkenine kaydet
        _user.user = request.user if request.user.is_authenticated else None
        response = self.get_response(request)

        # İşlem tamamlandığında kullanıcı bilgisini temizle
        _user.user = None
        return response
