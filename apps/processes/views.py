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
from .models import Part, PartProduction, Aircraft, PartOfAircraft, PartStock, AircraftProduction

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

            # Aircraft id'sine göre uçağı arıyoruz
            try:
                aircraft_type = Aircraft.objects.get(id=aircraft_id)
            except Aircraft.DoesNotExist:
                return JsonResponse({'message': 'Lütfen varolan uçaklardan bir tanesini seçin!'}, status=400)

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


class CreateAircraftView(ProcessesView):
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

            # Aircraft id'sine göre uçağı arıyoruz
            try:
                aircraft = Aircraft.objects.get(id=aircraft_id)
            except Aircraft.DoesNotExist:
                return JsonResponse({'message': 'Lütfen varolan uçaklardan bir tanesini seçin!'}, status=400)

            # Gerekli parçalar
            required_parts = ["Kanat", "Gövde", "Kuyruk", "Aviyonik"]
            missing_parts = []
            used_part_productions = []

            # Stok ve Parça Kontrolü
            for part_name in required_parts:
                part = Part.objects.get(name=part_name)
                part_stock = PartStock.objects.filter(part=part, aircraft_type=aircraft_id).first()

                if not part_stock or part_stock.quantity < 1:
                    missing_parts.append(part_name)
                else:
                    # Uygun part production kaydını al ve kullanılmak üzere listeye ekle
                    part_production = PartProduction.objects.filter(part=part, aircraft_type=aircraft_id,
                                                                    is_assembled=False, recycled_date__isnull=True,
                                                                    recycled_personal__isnull=True).first()
                    if part_production:
                        used_part_productions.append(part_production)

            # Eksik parça varsa montajı durdur ve uyarı ver
            if missing_parts:
                missing_parts_str = ", ".join(missing_parts)
                messages.error(request, f"Uçak üretimi için yeterli stok yok. Eksik parçalar: {missing_parts_str}")
                return JsonResponse({
                                        'message': f'Uçak üretimi için yeterli stok yok. Eksik parçalar: {missing_parts_str}. Lütfen önce bunlar üretilsin!'},
                                    status=400)
            if used_part_productions:
                aircraft_p = AircraftProduction()
                aircraft_p.complete_assembly(aircraft, request.user, used_part_productions)
                return JsonResponse({
                                        'message': f'Başarılı bir şekilde 1 adet {aircraft.name} uçağı oluşturuldu. Uçak id: {aircraft_p.id}'},
                                    status=200)

            else:
                missing_parts_str = ", ".join(missing_parts)
                used_parts_str = ", ".join(used_part_productions)
                return JsonResponse({
                                        'message': f'Bilinmedik bir hata! Eksik Parçalar {missing_parts_str}. Var olan parçalar: {used_parts_str}'},
                                    status=400)
        return JsonResponse({'message': 'Geçersiz istek.'}, status=400)


class ListAircraftView(ProcessesView):
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
                    "assembly_user": aircraft_production.assembly_user.username,
                    "assembly_date": aircraft_production.assembly_date.strftime('%d-%m-%Y %H:%M:%S'),
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
    return JsonResponse({"data": data})

def get_data_list_aircraft(request):
    aircraft_productions = AircraftProduction.objects.all()
    data = []

    for production in aircraft_productions:
        # Her uçak üretimi için kullanılan parçaların detaylarını içeren liste
        parts_used = {
            "kanat": None,
            "govde": None,
            "kuyruk": None,
            "aviyonik": None
        }

        # Uçağın tüm parçalarını `PartOfAircraft` modelinden alıyoruz
        parts = PartOfAircraft.objects.filter(aircraft_production=production)
        for part_of_aircraft in parts:
            part_type = convert_tr_to_en(part_of_aircraft.part_production.part.name.lower())  # Parça türünü belirlemek için
            if part_type in parts_used:
                parts_used[part_type] = {
                    "part_id": part_of_aircraft.part_production.id,
                    "producing_personal": part_of_aircraft.part_production.producing_personal.username if part_of_aircraft.part_production.producing_personal else "Bilinmiyor",
                    "produced_date": part_of_aircraft.part_production.produced_date.strftime('%d-%m-%Y %H:%M:%S') if part_of_aircraft.part_production.produced_date else "Bilinmiyor",
                }

        # Her uçak için ilgili bilgileri ekleyin
        data.append({
            "id": production.id,
            "aircraft_type": production.aircraft.name,
            "assembly_user": production.assembly_user.username if production.assembly_user else "Bilinmiyor",
            "assembly_date": production.assembly_date.strftime('%d-%m-%Y %H:%M:%S'),
            "parts_used": parts_used  # Kanat, Gövde, Kuyruk, Aviyonik bilgileri
        })

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
            part_production.recycle_part(user)

            return JsonResponse({"status": "ok", "message": "Parça başarıyla silindi."})

        except PartProduction.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Parça bulunamadı."})

    return JsonResponse({"status": "error", "message": "Geçersiz istek."})
