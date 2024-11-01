from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from apps.processes.models import Aircraft
from config import TemplateLayout

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""
from django.http import JsonResponse
from .models import Part, PartProduction, Aircraft, PartOfAircraft

from django.views.generic import TemplateView
from config import TemplateLayout
from config.template_helpers.theme import TemplateHelper

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to personals/urls.py file for more pages.
"""


def convert_tr_to_en(text):
    """Türkçe karakterleri İngilizce karakterlere çevirir."""
    tr_chars = "çğıöşü"
    en_chars = "cgiosu"
    translation_table = str.maketrans(tr_chars, en_chars)
    return text.translate(translation_table)


class ProcessesView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in config/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


def check_team_url_name(request, team_name):
    # Kullanıcının takımını alıyoruz ve İngilizceye çeviriyoruz
    user_team_name = convert_tr_to_en(request.user.personal.team.name.lower())
    url_team_name = convert_tr_to_en(team_name.lower())

    # Kullanıcının takımı ile URL'deki takım adı uyuşmazsa erişim izni verilmez
    if user_team_name != url_team_name:
        messages.add_message(request, messages.WARNING, "Bu sayfaya erişim yetkiniz yok.")
        return True
    return False


class CreateView(ProcessesView):
    def get(self, request, team_name):

        if check_team_url_name(request, team_name):
            return redirect('index')

        # Ekstra veriyi context ile gönderiyoruz
        context = self.get_context_data()
        context['title'] = request.user.personal.team.name  # 'title' anahtarına takım bilgisi ekleniyor
        context['aircraft'] = Aircraft.objects.all()  # 'title' anahtarına takım bilgisi ekleniyor
        return self.render_to_response(context)
        # return render(request, 'create.html', {'title': request.user.personal.team})

    def post(self, request, team_name):
        if request.method == "POST":

            if check_team_url_name(request, team_name):
                return redirect('index')

            # Uçak tipi bilgisi ve oturum açan kullanıcıyı alıyoruz
            aircraft_id = request.POST.get('aircraft_type')

            aircraft_type = Aircraft.objects.get(id=aircraft_id)  # Uçak tipi nesnesi

            # Kullanıcının takımı ve üretim yapacağı parça kontrolü
            team_name = request.user.personal.team.name
            if Part.objects.filter(name=team_name).exists():
                # Uygun part nesnesini bul ve üretim işlemini başlat
                part = Part.objects.get(name=team_name)
                part_production = PartProduction()
                part_production.produce_part(
                    user=request.user,
                    part=part,
                    aircraft_type=aircraft_type,
                    quantity=5
                )
                return JsonResponse({'message': 'Parça başarıyla üretildi!'})
            else:
                return JsonResponse({'message': 'Bu takımın parça üretme yetkisi yok.'}, status=403)

        return JsonResponse({'message': 'Geçersiz istek.'}, status=400)


class ListView(ProcessesView):
    def get(self, request, team_name):
        if check_team_url_name(request, team_name):
            return redirect('index')

        context = self.get_context_data()
        context['title'] = request.user.personal.team.name  # 'title' anahtarına takım bilgisi ekleniyor
        return self.render_to_response(context)
        # return render(request, 'create.html', {'title': request.user.personal.team})


def part_production_data(request):
    # Silinmemiş ve montaj bilgilerini içeren PartProduction kayıtlarını al
    part_productions = PartProduction.objects.filter(
        team_id=request.user.personal.team.id,
        recycled_date__isnull=True,
        recycled_personal__isnull=True
    )

    # JSON formatında veriyi hazırlama
    data = []
    for part in part_productions:
        # Parçanın montaj bilgilerini al
        assembly_info = ''
        if part.is_assembled:
            # `PartOfAircraft` modelinde `part_production` üzerinden montaj bilgilerini al
            part_of_aircraft = PartOfAircraft.objects.filter(part_production=part).first()
            if part_of_aircraft:
                # Montaj detaylarını `AircraftProduction` üzerinden al
                aircraft_production = part_of_aircraft.aircraft_production
                assembly_info = {
                    "aircraft_id": aircraft_production.aircraft.id,
                    "assembly_user": aircraft_production.assembly_user.id,
                    "assembly_date": aircraft_production.assembly_date.strftime('%d-%m-%Y H%:M%:S%'),
                }

        # Parça bilgilerini JSON formatına ekle
        data.append({
            "id": part.id,
            "producing_personal": part.producing_personal.username if part.producing_personal else "",
            "aircraft_type": part.aircraft_type.name if part.aircraft_type else "",
            "produced_date": part.produced_date.strftime('%d-%m-%Y %H:%M:%S'),
            "is_assembled": 'Evet' if part.is_assembled else 'Hayır',
            "assembly_info": assembly_info  # Montaj bilgileri (kullanıldıysa)
        })
    print(len(data), data)
    return JsonResponse({"data": data})


@csrf_exempt
def delete_part_production(request):
    if request.method == "POST":
        part_id = request.POST.get("id")
        user = request.user

        try:
            # PartProduction kaydını getir
            part_production = PartProduction.objects.get(id=part_id)

            # 1. Kullanıcının takım yetkisini kontrol et
            if part_production.team != user.personal.team:
                return JsonResponse({"status": "error", "message": "Bu parçayı silme yetkiniz yok."})

            # 2. Geri dönüşüm durumu kontrolü
            if part_production.recycled_date is not None or part_production.recycled_personal is not None:
                return JsonResponse({"status": "error", "message": "Bu parça zaten geri dönüşüme gönderilmiş."})

            # 3. Montaj durumu kontrolü
            if part_production.is_assembled:
                return JsonResponse({"status": "error", "message": "Bu parça bir uçakta montajlanmış ve silinemez."})

            # Tüm koşullar sağlanıyorsa, geri dönüşüm bilgilerini güncelle
            part_production.recycled_date = timezone.now()
            part_production.recycled_personal = user
            part_production.save()
            return JsonResponse({"status": "ok", "message": "Parça başarıyla silindi."})

        except PartProduction.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Parça bulunamadı."})

    return JsonResponse({"status": "error", "message": "Geçersiz istek."})