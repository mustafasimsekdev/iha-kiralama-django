from django.conf import settings


# Özel ayarları template context'ine ekler
def my_setting(request):
    # settings dosyasındaki tüm ayarları `MY_SETTING` anahtarı altında template'e gönderir
    return {'MY_SETTING': settings}


# Kullanıcının dil kodunu template context'ine ekler
def language_code(request):
    # Geçerli dil kodunu `LANGUAGE_CODE` anahtarı altında template'e gönderir
    return {"LANGUAGE_CODE": request.LANGUAGE_CODE}


# Çerezleri template context'ine ekler
def get_cookie(request):
    # Tüm çerezleri `COOKIES` anahtarı altında template'e gönderir
    return {"COOKIES": request.COOKIES}


# Ortam (development, production, vb.) ayarını template context'ine ekler
def environment(request):
    # settings dosyasındaki `ENVIRONMENT` ayarını `ENVIRONMENT` anahtarı altında template'e gönderir
    return {'ENVIRONMENT': settings.ENVIRONMENT}
