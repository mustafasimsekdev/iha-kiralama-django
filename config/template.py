# Template Settings
# ------------------------------------------------------------------------------


# Theme layout templates directory

# Template config
# ? Easily change the template configuration from here
# ? Replace this object with template-config/demo-*.py file's TEMPLATE_CONFIG to change the template configuration as per our demos
TEMPLATE_CONFIG = {
    "layout": "vertical",  # Options[String]: vertical(default), horizontal
    "theme": "theme-default",  # Options[String]: theme-default(default), theme-bordered, theme-semi-dark
    "style": "light",  # Options[String]: light(default), dark, system mode
    "rtl_support": True,  # options[Boolean]: True(default), False # To provide RTLSupport or not
    "rtl_mode": False,
    # options[Boolean]: False(default), True # To set layout to RTL layout  (myRTLSupport must be True for rtl mode)
    "has_customizer": True,
    # options[Boolean]: True(default), False # Display customizer or not THIS WILL REMOVE INCLUDED JS FILE. SO LOCAL STORAGE WON'T WORK
    "display_customizer": True,
    # options[Boolean]: True(default), False # Display customizer UI or not, THIS WON'T REMOVE INCLUDED JS FILE. SO LOCAL STORAGE WILL WORK
    "content_layout": "compact",  # options[String]: 'compact', 'wide' (compact=container-xxl, wide=container-fluid)
    "navbar_type": "fixed",  # options[String]: 'fixed', 'static', 'hidden' (Only for vertical Layout)
    "header_type": "fixed",  # options[String]: 'static', 'fixed' (for horizontal layout only)
    "menu_fixed": True,  # options[Boolean]: True(default), False # Layout(menu) Fixed (Only for vertical Layout)
    "menu_collapsed": False,  # options[Boolean]: False(default), True # Show menu collapsed, Only for vertical Layout
    "footer_fixed": False,  # options[Boolean]: False(default), True # Footer Fixed
    "show_dropdown_onhover": True,  # True, False (for horizontal layout only)
    "customizer_controls": [
        "rtl",
        "style",
        "headerType",
        "contentLayout",
        "layoutCollapsed",
        "showDropdownOnHover",
        "layoutNavbarOptions",
        "themes",
    ],  # To show/hide customizer options
}

# Theme Variables
# ? Personalize template by changing theme variables (For ex: Name, URL Version etc...)
THEME_VARIABLES = {
    "creator_name": "MustafaSimsek",
    "creator_url": "https://www.linkedin.com/in/mustafasimsekdev",
    "template_name": "İHA Kiralama",
    "template_suffix": "Django",
    "template_description": "İHA (İnsansız Hava Aracı) Kiralama ve Üretim Yönetimi Projesi: Django kullanarak personel, parça, takım ve uçak üretim süreçlerini yönetmeyi sağlayan, server-side ve client-side destekli modern bir yönetim platformu. Takım bazlı parça üretimi, envanter kontrolü, montaj işlemleri ve eksik parça uyarıları gibi fonksiyonları içeren kapsamlı bir çözüm.",
    "template_keyword": "iha kiralama, insansız hava aracı yönetimi, django proje, parça üretim yönetimi, envanter kontrolü, montaj takımı yönetimi, server-side ve client-side destek, uçak üretim süreci, takımlar bazında yönetim, eksik parça uyarıları",
    "twitter_url": "https://x.com/mustafasimsekpy",
    "github_url": "https://github.com/mustafasimsekdev",
    "linkedin_url": "https://www.linkedin.com/in/mustafasimsekdev",
    "git_repository": "iha-kiralama-django",
    "git_repo_access": "https://tools.pixinvent.com/github/github-access",
}

# ! Don't change THEME_LAYOUT_DIR unless it's required
THEME_LAYOUT_DIR = "layout"
