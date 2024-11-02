from django.views.generic import TemplateView
from config import TemplateLayout
from config.template_helpers.theme import TemplateHelper

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages


# Authentication ile ilgili view
class AuthView(TemplateView):
    # Varsayılan olarak context verisini hazırlayan fonksiyon
    def get_context_data(self, **kwargs):
        # Global layout'u başlatan bir fonksiyon
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # Context'i güncelleme işlemi
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
            }
        )

        return context  # Güncellenmiş context'i döndür


# Login işlemleri için view
class LoginView(AuthView):
    def get(self, request):
        # Eğer kullanıcı zaten giriş yapmışsa, ana sayfaya yönlendirilir
        if request.user.is_authenticated:
            return redirect("index")  # 'index' ana sayfa için URL adı

        # Eğer kullanıcı giriş yapmamışsa login sayfası render edilir
        return super().get(request)

    def post(self, request):
        if request.method == "POST":
            # Kullanıcı adı veya e-posta ve şifreyi formdan alır
            username = request.POST.get("email-username")
            password = request.POST.get("password")

            # Kullanıcı adı veya şifre boşsa hata mesajı verir ve login sayfasına yönlendirir
            if not (username and password):
                messages.error(request, "Lütfen kullanıcı adınızı ve şifrenizi giriniz.")
                return redirect("login")

            # Eğer kullanıcı adı bir e-posta adresiyse, e-posta ile kullanıcıyı bulur
            if "@" in username:
                user_email = User.objects.filter(email=username).first()
                if user_email is None:
                    messages.error(request, "Lütfen geçerli bir e-posta adresi giriniz.")
                    return redirect("login")
                username = user_email.username

            # Kullanıcı adı veritabanında yoksa hata mesajı verir
            user_email = User.objects.filter(username=username).first()
            if user_email is None:
                messages.error(request, "Lütfen geçerli bir kullanıcı adı giriniz.")
                return redirect("login")

            # Kullanıcıyı doğrulama (authenticate) işlemi
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                # Giriş başarılıysa kullanıcıyı giriş yapmış olarak işaretler
                login(request, authenticated_user)

                # Eğer 'next' parametresi varsa kullanıcıyı o sayfaya yönlendirir
                if "next" in request.POST:
                    return redirect(request.POST["next"])
                else:
                    # Aksi halde ana sayfaya yönlendirir
                    return redirect("index")
            else:
                # Doğrulama başarısızsa hata mesajı verir
                messages.error(request, "Lütfen geçerli bir kullanıcı adı giriniz.")
                return redirect("login")
