from django.conf import settings
from pprint import pprint
import os
from importlib import import_module, util


# Temel şablon yardımcı sınıfı
class TemplateHelper:
    # Şablon context'ini TEMPLATE_CONFIG ile başlatan fonksiyon
    def init_context(context):
        # settings.TEMPLATE_CONFIG'ten değerleri context'e ekler
        context.update(
            {
                "layout": settings.TEMPLATE_CONFIG.get("layout"),
                "theme": settings.TEMPLATE_CONFIG.get("theme"),
                "style": settings.TEMPLATE_CONFIG.get("style"),
                "rtl_support": settings.TEMPLATE_CONFIG.get("rtl_support"),
                "rtl_mode": settings.TEMPLATE_CONFIG.get("rtl_mode"),
                "has_customizer": settings.TEMPLATE_CONFIG.get("has_customizer"),
                "display_customizer": settings.TEMPLATE_CONFIG.get(
                    "display_customizer"
                ),
                "content_layout": settings.TEMPLATE_CONFIG.get("content_layout"),
                "navbar_type": settings.TEMPLATE_CONFIG.get("navbar_type"),
                "header_type": settings.TEMPLATE_CONFIG.get("header_type"),
                "menu_fixed": settings.TEMPLATE_CONFIG.get("menu_fixed"),
                "menu_collapsed": settings.TEMPLATE_CONFIG.get("menu_collapsed"),
                "footer_fixed": settings.TEMPLATE_CONFIG.get("footer_fixed"),
                "show_dropdown_onhover": settings.TEMPLATE_CONFIG.get(
                    "show_dropdown_onhover"
                ),
                "customizer_controls": settings.TEMPLATE_CONFIG.get(
                    "customizer_controls"
                ),
            }
        )
        return context

    # Şablon sınıfı/değeri/değişken adları ile context değişkenlerini eşleştirir
    def map_context(context):
        # Yatay layout için header tipi ayarları
        if context.get("layout") == "horizontal":
            if context.get("header_type") == "fixed":
                context["header_type_class"] = "layout-menu-fixed"
            elif context.get("header_type") == "static":
                context["header_type_class"] = ""
            else:
                context["header_type_class"] = ""
        else:
            context["header_type_class"] = ""

        # Navbar tipi ayarları (dikey/front destekli)
        if context.get("layout") != "horizontal":
            if context.get("navbar_type") == "fixed":
                context["navbar_type_class"] = "layout-navbar-fixed"
            elif context.get("navbar_type") == "static":
                context["navbar_type_class"] = ""
            else:
                context["navbar_type_class"] = "layout-navbar-hidden"
        else:
            context["navbar_type_class"] = ""

        # Menü sıkıştırılmış mı?
        context["menu_collapsed_class"] = (
            "layout-menu-collapsed" if context.get("menu_collapsed") else ""
        )

        # Dikey layout için menü sabit mi?
        if context.get("layout") == "vertical":
            if context.get("menu_fixed") is True:
                context["menu_fixed_class"] = "layout-menu-fixed"
            else:
                context["menu_fixed_class"] = ""

        # Footer sabit mi?
        context["footer_fixed_class"] = (
            "layout-footer-fixed" if context.get("footer_fixed") else ""
        )

        # RTL destekli şablon
        context["rtl_support_value"] = "/rtl" if context.get("rtl_support") else ""

        # RTL modu ve metin yönü
        context["rtl_mode_value"], context["text_direction_value"] = (
            ("rtl", "rtl") if context.get("rtl_mode") else ("ltr", "ltr")
        )

        # Yatay menüde dropdown'u hover ile gösterme
        context["show_dropdown_onhover_value"] = (
            "true" if context.get("show_dropdown_onhover") else "false"
        )

        # Özelleştirici gösteriliyor mu?
        context["display_customizer_class"] = (
            "" if context.get("display_customizer") else "customizer-hide"
        )

        # İçerik layout'u geniş mi, dar mı?
        if context.get("content_layout") == "wide":
            context["container_class"] = "container-fluid"
            context["content_layout_class"] = "layout-wide"
        else:
            context["container_class"] = "container-xxl"
            context["content_layout_class"] = "layout-compact"

        # Navbar ayrık mı?
        if context.get("navbar_detached") == True:
            context["navbar_detached_class"] = "navbar-detached"
        else:
            context["navbar_detached_class"] = ""

    # Belirli bir kapsamda tema değişkenlerini döner
    def get_theme_variables(scope):
        return settings.THEME_VARIABLES[scope]

    # Belirli bir kapsamda tema yapılandırmasını döner
    def get_theme_config(scope):
        return settings.TEMPLATE_CONFIG[scope]

    # Geçerli sayfa layout'unu ayarlar ve layout bootstrap dosyasını başlatır
    def set_layout(view, context={}):
        # Görünüm yolundan layout'u çıkar
        layout = os.path.splitext(view)[0].split("/")[0]

        # Modül yolunu al
        module = f"templates.{settings.THEME_LAYOUT_DIR.replace('/', '.')}.bootstrap.{layout}"

        # Eğer bootstrap dosyası varsa otomatik import ve başlatma yapar
        if util.find_spec(module) is not None:
            TemplateBootstrap = TemplateHelper.import_class(
                module, f"TemplateBootstrap{layout.title().replace('_', '')}"
            )
            TemplateBootstrap.init(context)
        else:
            # Eğer bootstrap dosyası yoksa default bootstrap'i kullanır
            module = f"templates.{settings.THEME_LAYOUT_DIR.replace('/', '.')}.bootstrap.default"

            TemplateBootstrap = TemplateHelper.import_class(
                module, "TemplateBootstrapDefault"
            )
            TemplateBootstrap.init(context)

        return f"{settings.THEME_LAYOUT_DIR}/{view}"

    # Modülü string ile import eder
    def import_class(fromModule, import_className):
        module = import_module(fromModule)
        return getattr(module, import_className)
