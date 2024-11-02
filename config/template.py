# Template Ayarlar
# ------------------------------------------------------------------------------


# Tema düzeni şablonları için dizin
# THEME_LAYOUT_DIR, şablonların bulunduğu dizini belirtir ve burada `layout` olarak ayarlanmıştır
# Bu ayarı değiştirmek yalnızca gerekli olduğunda yapılmalıdır
THEME_LAYOUT_DIR = "layout"

# Tema yapılandırma ayarları
# Bu bölüm, şablonun genel yapılandırmasını kolayca değiştirebilmek için ayarları içerir
# Ayarlar `TEMPLATE_CONFIG` nesnesinde yapılandırılmıştır ve değiştirilebilir

TEMPLATE_CONFIG = {
    "layout": "vertical",  # Sayfa düzeni. Opsiyonlar[String]: vertical(default), horizontal
    "theme": "theme-default",
    # Tema seçeneği. Opsiyonlar[String]: theme-default(default), theme-bordered, theme-semi-dark
    "style": "light",  # Renk stili. Opsiyonlar[String]: light(default), dark, system mode
    "rtl_support": True,  # RTL (Sağdan Sola) desteği sağlar mı? Opsiyonlar[Boolean]: True(default), False
    "rtl_mode": False,  # RTL modu etkinleştirildi mi? rtl_support True olmalı
    "has_customizer": True,  # Özelleştirici görünüyor mu? Opsiyonlar[Boolean]: True(default), False
    "display_customizer": True,  # Özelleştirici UI görüntüleniyor mu? Opsiyonlar[Boolean]: True(default), False
    "content_layout": "compact",  # İçerik düzeni. Opsiyonlar[String]: 'compact', 'wide'
    "navbar_type": "fixed",  # Navbar tipi. Opsiyonlar[String]: 'fixed', 'static', 'hidden' (Sadece dikey düzen için)
    "header_type": "fixed",  # Başlık tipi. Opsiyonlar[String]: 'static', 'fixed' (Yatay düzen için)
    "menu_fixed": True,  # Menü sabit mi? Opsiyonlar[Boolean]: True(default), False (Sadece dikey düzen için)
    "menu_collapsed": False,  # Menü başlangıçta sıkıştırılmış mı? Opsiyonlar[Boolean]: False(default), True
    "footer_fixed": False,  # Footer sabit mi? Opsiyonlar[Boolean]: False(default), True
    "show_dropdown_onhover": True,  # Dropdown hover ile görüntülensin mi? (Sadece yatay düzen için)
    "customizer_controls": [
        "rtl",
        "style",
        "headerType",
        "contentLayout",
        "layoutCollapsed",
        "showDropdownOnHover",
        "layoutNavbarOptions",
        "themes",
    ],  # Özelleştiricide gösterilecek seçenekler listesi
}

# Tema değişkenleri
# Bu bölüm, şablon hakkında kişisel bilgileri, URL'leri ve açıklamaları içerir
# Tema üzerinde kişisel dokunuşlar yapmanızı sağlar

THEME_VARIABLES = {
    "creator_name": "MustafaSimsek",  # Oluşturan kişinin adı
    "creator_url": "https://www.linkedin.com/in/mustafasimsekdev",  # Oluşturanın bağlantı URL'si
    "template_name": "İHA Kiralama",  # Şablon adı
    "template_suffix": "Django",  # Şablonun suffix bilgisi
    "template_description": "İHA (İnsansız Hava Aracı) Kiralama ve Üretim Yönetimi Projesi: Django kullanarak personel, parça, takım ve uçak üretim süreçlerini yönetmeyi sağlayan, server-side ve client-side destekli modern bir yönetim platformu. Takım bazlı parça üretimi, envanter kontrolü, montaj işlemleri ve eksik parça uyarıları gibi fonksiyonları içeren kapsamlı bir çözüm.",
    # Şablon açıklaması
    "template_keyword": "iha kiralama, insansız hava aracı yönetimi, django proje, parça üretim yönetimi, envanter kontrolü, montaj takımı yönetimi, server-side ve client-side destek, uçak üretim süreci, takımlar bazında yönetim, eksik parça uyarıları",
    # Şablon için anahtar kelimeler
    "twitter_url": "https://x.com/mustafasimsekpy",  # Twitter URL'si
    "github_url": "https://github.com/mustafasimsekdev",  # GitHub URL'si
    "linkedin_url": "https://www.linkedin.com/in/mustafasimsekdev",  # LinkedIn URL'si
    "git_repository": "iha-kiralama-django"  # GitHub repo adı
}
