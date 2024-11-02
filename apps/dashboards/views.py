from django.views.generic import TemplateView
from config import TemplateLayout


class DashboardsView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in config/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context
