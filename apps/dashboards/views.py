from django.views.generic import TemplateView
from config import TemplateLayout


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""


class DashboardsView(TemplateView):
    print("run DashboardsView")
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in config/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context