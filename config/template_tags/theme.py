from django.utils.safestring import mark_safe
from django import template
from config.template_helpers.theme import TemplateHelper
from django.contrib.auth.decorators import user_passes_test

register = template.Library()  # Django'nun template tag kayıt mekanizmasını başlatır


# Theme sınıfını HTML şablonlarda kullanabilmek için tag'leri kaydediyoruz

# Tema değişkenlerini almak için kullanılan custom template tag
@register.simple_tag
def get_theme_variables(scope):
    # Tema değişkenlerini alır ve güvenli bir şekilde HTML içinde kullanıma izin verir
    return mark_safe(TemplateHelper.get_theme_variables(scope))


# Tema yapılandırmasını almak için kullanılan custom template tag
@register.simple_tag
def get_theme_config(scope):
    return mark_safe(TemplateHelper.get_theme_config(scope))


# URL'ye göre alt menüleri filtreleyen custom filter
@register.filter
def filter_by_url(submenu, url):
    if submenu:
        for subitem in submenu:
            subitem_url = subitem.get("url")
            if subitem_url == url.path or subitem_url == url.resolver_match.url_name:
                return True

            # Eğer submenu'nun içinde başka bir submenu varsa, onu da recursive olarak kontrol eder
            elif subitem.get("submenu"):
                if filter_by_url(subitem["submenu"], url):
                    return True

    # Hiçbir eşleşme yoksa False döner
    return False


# Kullanıcının belirli bir gruba sahip olup olmadığını kontrol eden custom filter
@register.filter
def has_group(user, group):
    if user.groups.filter(name=group).exists():  # Belirli bir grup adını kontrol eder
        return True


# Kullanıcının belirli bir izne sahip olup olmadığını kontrol eden custom filter
@register.filter
def has_permission(user, permission):
    if user.has_perm(permission):  # Kullanıcının izne sahip olup olmadığını kontrol eder
        return True


# Kullanıcının "admin" grubunda olup olmadığını kontrol eden custom filter
@register.filter(name="is_admin")
def is_admin(user):
    return user.groups.filter(name="admin").exists()


# "admin" grubunda olmayı gerektiren view'ler için decorator
@register.filter(name="admin_required")
def admin_required(view_func):
    # is_admin fonksiyonunu geçemezse login sayfasına yönlendirilir
    return user_passes_test(is_admin, login_url='login')(view_func)


# Kullanıcının "client" grubunda olup olmadığını kontrol eden custom filter
@register.filter(name="is_client")
def is_client(user):
    return user.groups.filter(name="client").exists()


# "client" grubunda olmayı gerektiren view'ler için decorator
@register.filter(name="client_required")
def client_required(view_func):
    # is_client fonksiyonunu geçemezse login sayfasına yönlendirilir
    return user_passes_test(is_client, login_url='login')(view_func)


# Kullanıcının süper kullanıcı olup olmadığını kontrol eden custom filter
@register.filter(name="is_superuser")
def is_superuser(user):
    return user.is_superuser


# Süper kullanıcı olmayı gerektiren view'ler için decorator
@register.filter(name="superuser_required")
def superuser_required(view_func):
    return user_passes_test(is_superuser, login_url='login')(view_func)


# Kullanıcının staff olup olmadığını kontrol eden custom filter
@register.filter(name="is_staff")
def is_staff(user):
    return user.is_staff


# Staff olmayı gerektiren view'ler için decorator
@register.filter(name="staff_required")
def staff_required(view_func):
    # is_staff fonksiyonunu geçemezse login sayfasına yönlendirilir
    return user_passes_test(is_staff, login_url='login')(view_func)


# Geçerli URL'yi döndüren custom template tag
@register.simple_tag
def current_url(request):
    return request.build_absolute_uri()
