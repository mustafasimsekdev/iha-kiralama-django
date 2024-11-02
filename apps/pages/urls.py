from django.urls import path
from .views import PagesView
from .views_misc import MiscPagesView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "pages/account_settings/account/",
        login_required(PagesView.as_view(template_name="pages_account_settings_account.html")),
        name="pages-account-settings-account",
    ),

]
