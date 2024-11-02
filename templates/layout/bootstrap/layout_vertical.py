from django.conf import settings
import json

from config.middlewares import get_current_user
from config.template_helpers.theme import TemplateHelper

menu_file_path =  settings.BASE_DIR / "templates" / "layout" / "partials" / "menu" / "vertical" / "json" / "vertical_menu.json"

"""
This is an entry and Bootstrap class for the theme level.
The init() function will be called in config/__init__.py
"""


class TemplateBootstrapLayoutVertical:
    def init(context):
        context.update(
            {
                "layout": "vertical",
                "content_navbar": True,
                "is_navbar": True,
                "is_menu": True,
                "is_footer": True,
                "navbar_detached": True,
            }
        )

        # map_context according to updated context values
        TemplateHelper.map_context(context)

        TemplateBootstrapLayoutVertical.init_menu_data(context)

        return context

    def init_menu_data(context):
        # Load the menu data from the JSON file
        menu_data = []
        if menu_file_path.exists():
            with open(menu_file_path, "r", encoding="utf-8") as file:
                menu_data = json.load(file)

        # Get user team from context
        user = get_current_user()

        if user:
            team_name = user.personal.team.name

            # Filter menu based on team
            filtered_menu = TemplateBootstrapLayoutVertical.filter_menu_by_team(menu_data, team_name)
        else:
            filtered_menu = []

        # Update context with filtered menu data
        context.update({"menu_data": filtered_menu})

    @staticmethod
    def filter_menu_by_team(menu_data, team_name):
        """Takım adına göre menüyü filtreler."""
        if not team_name:
            return []  # Geçerli bir takım yoksa boş menü döner

        filtered_menu = []
        for menu in menu_data["menu"]:
            # submenu öğelerini takım adına göre filtrele
            filtered_submenu = [
                submenu for submenu in menu.get("submenu", [])
                if team_name in submenu.get("teams", [])
            ]

            # Eğer submenu'de takımın erişebileceği öğeler varsa, menüye ekle
            if filtered_submenu:
                # Ana menü öğesini kopyalayarak sadece erişilebilir submenu öğelerini ekle
                filtered_menu_item = menu.copy()
                filtered_menu_item["submenu"] = filtered_submenu
                filtered_menu.append(filtered_menu_item)

        return filtered_menu


