from django.urls import path
from .views import CreateView, ListView, part_production_data, delete_part_production

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        'create/<str:team_name>/',
        login_required(CreateView.as_view(template_name="create.html"), ),
        name="create_part",
    ),
    path(
        'list/<str:team_name>/',
        login_required(ListView.as_view(template_name="list.html"), ),
        name="list_part",
    ),
    path('part-productions/data/', login_required(part_production_data), name='part_production_data'),

    path('part-productions/delete/', login_required(delete_part_production), name='delete_part_production'),

    path(
        'create/aircraft/',
        login_required(CreateAircraftView.as_view(template_name="create-aircraft.html"), ),
        name="create_part",
    ),

]
