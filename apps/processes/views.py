from django.http import JsonResponse
from .models import Part, PartProduction, Aircraft, PartOfAircraft, PartStock, AircraftProduction
from django.views.generic import TemplateView
from config import TemplateLayout
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


def convert_tr_to_en(text):
    """Türkçe karakterleri İngilizce karakterlere çevirir."""
    tr_chars = "çğıöşü"
    en_chars = "cgiosu"
    translation_table = str.maketrans(tr_chars, en_chars)
    return text.translate(translation_table)


# Uygulamanın genel layout ayarlarını başlatan ve context verilerini düzenleyen bir view
class ProcessesView(TemplateView):
    # Context verilerini düzenleyen Django'nun hazırda tanımlı bir fonksiyonu
    def get_context_data(self, **kwargs):
        # Global layout ayarlarını başlatan özel bir fonksiyon, config/__init__.py içinde tanımlıdır
        # TemplateLayout.init(context) ifadesi ile context, uygulamanın genel layout ayarlarına göre güncellenir
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


# Kullanıcının takım ismi ile URL'deki takım ismini karşılaştıran fonksiyon
def check_team_url_name(request, team_name):
    # Kullanıcının takımını alıyoruz ve Türkçe karakterleri İngilizceye çeviriyoruz
    user_team_name = convert_tr_to_en(request.user.personal.team.name.lower())
    # URL'den gelen takım ismini de Türkçe karakterlerden İngilizce karakterlere çeviriyoruz
    url_team_name = convert_tr_to_en(team_name.lower())

    # Kullanıcının takımı ile URL'deki takım adı uyuşmazsa erişim izni verilmez
    if user_team_name != url_team_name:
        messages.add_message(request, messages.WARNING, "Bu sayfaya erişim yetkiniz yok.")
        # True döndürerek erişimin reddedilmesi gerektiğini belirtiriz
        return True

    # Uyuşma durumunda False döndürerek erişime izin verildiğini belirtiriz
    return False


# Parça üretim süreci için view
class CreateView(ProcessesView):
    def get(self, request, team_name):
        # Kullanıcının URL ile uyumlu bir takımda olup olmadığını kontrol eder
        if check_team_url_name(request, team_name):
            return redirect('index')  # Yetkisiz kullanıcılar ana sayfaya yönlendirilir

        # Context verisini hazırlayıp takıma ve uçak listesine göre gönderiyoruz
        context = self.get_context_data()
        context['title'] = request.user.personal.team.name  # Kullanıcının takım adı
        context['aircraft'] = Aircraft.objects.all()  # Tüm uçak kayıtları
        return self.render_to_response(context)  # Şablona context verisiyle render eder

    def post(self, request, team_name):
        if request.method == "POST":

            # Kullanıcının URL ile uyumlu bir takımda olup olmadığını kontrol eder
            if check_team_url_name(request, team_name):
                return redirect('index')

            # Formdan uçak tipi ID'sini alır
            aircraft_id = request.POST.get('aircraft_type')

            # Gönderilen aircraft_id'ye göre uçak nesnesini alır
            try:
                aircraft_type = Aircraft.objects.get(id=aircraft_id)
            except Aircraft.DoesNotExist:
                # Uçak bulunamazsa hata mesajı döner
                return JsonResponse({'message': 'Lütfen varolan uçaklardan bir tanesini seçin!'}, status=400)

            # Kullanıcının takım adını alır ve bu takıma ait bir parçanın olup olmadığını kontrol eder
            team_name = request.user.personal.team.name

            if Part.objects.filter(name=team_name).exists():
                # Takıma özel bir parça bulup üretim işlemini başlatır
                part = Part.objects.get(name=team_name)
                part_production = PartProduction()
                part_production.produce_part(
                    user=request.user,
                    part=part,
                    aircraft_type=aircraft_type,
                )
                # Başarılı üretim mesajı döner
                return JsonResponse({'message': 'Parça başarıyla üretildi!'})
            else:
                # Yetkisiz takım mesajı döner
                return JsonResponse({'message': 'Bu takımın parça üretme yetkisi yok.'}, status=403)

        # POST dışındaki isteklere hata mesajı döner
        return JsonResponse({'message': 'Geçersiz istek.'}, status=400)


# Parçaları listeleyen view
class ListView(ProcessesView):
    def get(self, request, team_name):
        # Kullanıcının URL ile uyumlu bir takımda olup olmadığını kontrol eder
        if check_team_url_name(request, team_name):
            return redirect('index')

        # Context verisini hazırlayıp kullanıcının takım adını ekler
        context = self.get_context_data()
        context['title'] = request.user.personal.team.name
        return self.render_to_response(context)


class CreateAircraftView(ProcessesView):
    def get(self, request, team_name):
        # Kullanıcının URL ile uyumlu bir takımda olup olmadığını kontrol eder
        if check_team_url_name(request, team_name):
            return redirect('index')  # Yetkisiz kullanıcılar ana sayfaya yönlendirilir

        # Context verisini hazırlayıp takıma ve uçak listesine göre gönderiyoruz
        context = self.get_context_data()
        context['title'] = request.user.personal.team.name
        context['aircraft'] = Aircraft.objects.all()
        return self.render_to_response(context)

    def post(self, request, team_name):
        if request.method == "POST":
            # Kullanıcının URL ile uyumlu bir takımda olup olmadığını kontrol eder
            if check_team_url_name(request, team_name):
                return redirect('index')

            # Formdan uçak tipi ID'sini alır
            aircraft_id = request.POST.get('aircraft_type')

            # Gönderilen aircraft_id'ye göre uçak nesnesini alır
            try:
                aircraft = Aircraft.objects.get(id=aircraft_id)
            except Aircraft.DoesNotExist:
                # Uçak bulunamazsa hata mesajı döner
                return JsonResponse({'message': 'Lütfen varolan uçaklardan bir tanesini seçin!'}, status=400)

            # Montaj için gerekli parçalar
            required_parts = ["Kanat", "Gövde", "Kuyruk", "Aviyonik"]
            missing_parts = []  # Eksik parçalar listesi
            used_part_productions = []  # Kullanılacak parçaların üretim kayıtları

            # Her gerekli parça için stok ve üretim kontrolü yapar
            for part_name in required_parts:
                part = Part.objects.get(name=part_name)  # Parça kaydını alır
                part_stock = PartStock.objects.filter(part=part, aircraft_type=aircraft_id).first()

                # Stok miktarını kontrol eder
                if not part_stock or part_stock.quantity < 1:
                    missing_parts.append(part_name)  # Yeterli stok yoksa eksik parçalara ekler
                else:
                    # Uygun bir PartProduction kaydını alır ve kullanılmak üzere listeye ekler
                    part_production = PartProduction.objects.filter(part=part, aircraft_type=aircraft_id,
                                                                    is_assembled=False, recycled_date__isnull=True,
                                                                    recycled_personal__isnull=True).first()
                    if part_production:
                        used_part_productions.append(part_production)  # Kullanılacak parçayı listeye ekler

            # Eğer eksik parçalar varsa montajı durdurur ve uyarı mesajı döner
            if missing_parts:
                missing_parts_str = ", ".join(missing_parts)
                messages.error(request, f"Uçak üretimi için yeterli stok yok. Eksik parçalar: {missing_parts_str}")
                return JsonResponse({
                    'message': f'Uçak üretimi için yeterli stok yok. Eksik parçalar: {missing_parts_str}. Lütfen önce bunlar üretilsin!'},
                    status=400)

            # Eğer kullanılabilir parçalar mevcutsa montaj işlemini başlatır
            if used_part_productions:
                aircraft_p = AircraftProduction()
                aircraft_p.complete_assembly(aircraft, request.user, used_part_productions)
                return JsonResponse({
                    'message': f'Başarılı bir şekilde 1 adet {aircraft.name} uçağı oluşturuldu. Uçak id: {aircraft_p.id}'},
                    status=200)

            else:
                # Bilinmeyen bir hata durumunda hata mesajı döner
                missing_parts_str = ", ".join(missing_parts)
                used_parts_str = ", ".join(used_part_productions)
                return JsonResponse({
                    'message': f'Bilinmedik bir hata! Eksik Parçalar {missing_parts_str}. Var olan parçalar: {used_parts_str}'},
                    status=400)

        # POST dışındaki isteklere hata mesajı döner
        return JsonResponse({'message': 'Geçersiz istek.'}, status=400)


# Uçakları listeleyen view
class ListAircraftView(ProcessesView):
    def get(self, request, team_name):
        # Kullanıcının URL ile uyumlu bir takımda olup olmadığını kontrol eder
        if check_team_url_name(request, team_name):
            return redirect('index')

        # Context verisini hazırlayıp kullanıcının takım adını ekler
        context = self.get_context_data()
        context['title'] = request.user.personal.team.name
        return self.render_to_response(context)  # Şablona context verisiyle render eder


# PartProduction kayıtlarını JSON formatında dönen fonksiyon
def part_production_data(request):
    # Sadece oturum açmış kullanıcının takımına ait, geri dönüştürülmemiş ve montaj edilmemiş parçaları filtrele
    part_productions = PartProduction.objects.filter(
        team_id=request.user.personal.team.id,
        recycled_date__isnull=True,
        recycled_personal__isnull=True
    )

    # JSON formatında veriyi hazırlama
    data = []
    for part in part_productions:
        # Parçanın montaj bilgilerini kontrol et
        assembly_info = ''
        if part.is_assembled:
            # `PartOfAircraft` modelinde bu parçaya ait montaj kaydını al
            part_of_aircraft = PartOfAircraft.objects.filter(part_production=part).first()
            if part_of_aircraft:
                # Montaj işleminin detaylarını `AircraftProduction` üzerinden al
                aircraft_production = part_of_aircraft.aircraft_production
                assembly_info = {
                    "aircraft_id": aircraft_production.aircraft.id,
                    "assembly_user": aircraft_production.assembly_user.username,
                    "assembly_date": aircraft_production.assembly_date.strftime('%d-%m-%Y %H:%M:%S'),
                }

        # Parça üretim bilgilerini JSON formatına ekle
        data.append({
            "id": part.id,
            "producing_personal": part.producing_personal.username if part.producing_personal else "",
            "aircraft_type": part.aircraft_type.name if part.aircraft_type else "",
            "produced_date": part.produced_date.strftime('%d-%m-%Y %H:%M:%S'),
            "is_assembled": 'Evet' if part.is_assembled else 'Hayır',
            "assembly_info": assembly_info  # Montaj bilgileri (kullanıldıysa)
        })

    # JSON formatında veri döndür
    return JsonResponse({"data": data})


# Tüm uçak üretimlerini ve ilgili parçaları listeleyen fonksiyon
def get_data_list_aircraft(request):
    # Tüm uçak üretim kayıtlarını al
    aircraft_productions = AircraftProduction.objects.all()
    data = []

    for production in aircraft_productions:
        # Her uçak üretimi için kullanılan parçaların detaylarını tutan bir sözlük
        parts_used = {
            "kanat": None,
            "govde": None,
            "kuyruk": None,
            "aviyonik": None
        }

        # Uçağın tüm parçalarını `PartOfAircraft` modelinden alıyoruz
        parts = PartOfAircraft.objects.filter(aircraft_production=production)
        for part_of_aircraft in parts:
            # Parça türünü belirlemek için parçanın adını İngilizce karakterlere çeviriyoruz
            part_type = convert_tr_to_en(
                part_of_aircraft.part_production.part.name.lower())

            # Eğer parça türü 'kanat', 'govde', 'kuyruk' veya 'aviyonik' ise ilgili bilgi sözlüğe eklenir
            if part_type in parts_used:
                parts_used[part_type] = {
                    "part_id": part_of_aircraft.part_production.id,
                    "producing_personal": part_of_aircraft.part_production.producing_personal.username if part_of_aircraft.part_production.producing_personal else "Bilinmiyor",
                    "produced_date": part_of_aircraft.part_production.produced_date.strftime(
                        '%d-%m-%Y %H:%M:%S') if part_of_aircraft.part_production.produced_date else "Bilinmiyor",
                }

        # Her uçak üretim kaydı için JSON formatında bilgi eklenir
        data.append({
            "id": production.id,
            "aircraft_type": production.aircraft.name,
            "assembly_user": production.assembly_user.username if production.assembly_user else "Bilinmiyor",
            "assembly_date": production.assembly_date.strftime('%d-%m-%Y %H:%M:%S'),
            "parts_used": parts_used  # Kanat, Gövde, Kuyruk, Aviyonik bilgileri
        })

    # JSON formatında veri döndür
    return JsonResponse({"data": data})


# Parça geri dönüşüm işlemi yapan fonksiyon
@csrf_exempt
def delete_part_production(request):
    if request.method == "POST":
        part_id = request.POST.get("id")
        user = request.user

        try:
            # PartProduction kaydını veritabanından alır
            part_production = PartProduction.objects.get(id=part_id)

            # 1. Kullanıcının takım yetkisini kontrol et
            # Parçayı silmeye çalışanın takımının, parçanın takımına eşit olup olmadığını kontrol eder
            if part_production.team != user.personal.team:
                return JsonResponse({"status": "error", "message": "Bu parçayı silme yetkiniz yok."})

            # 2. Geri dönüşüm durumu kontrolü
            # Eğer parça zaten geri dönüşüme gönderilmişse hata döner
            if part_production.recycled_date is not None or part_production.recycled_personal is not None:
                return JsonResponse({"status": "error", "message": "Bu parça zaten geri dönüşüme gönderilmiş."})

            # 3. Montaj durumu kontrolü
            # Eğer parça bir uçakta montajlanmışsa silinemez
            if part_production.is_assembled:
                return JsonResponse({"status": "error", "message": "Bu parça bir uçakta montajlanmış ve silinemez."})

            # Tüm koşullar sağlanıyorsa, geri dönüşüm bilgilerini günceller
            part_production.recycle_part(user)

            return JsonResponse({"status": "ok", "message": "Parça başarıyla silindi."})

        except PartProduction.DoesNotExist:
            # Eğer belirtilen ID'ye sahip bir PartProduction bulunamazsa hata döner
            return JsonResponse({"status": "error", "message": "Parça bulunamadı."})

    # POST dışındaki istekler için geçersiz istek mesajı döner
    return JsonResponse({"status": "error", "message": "Geçersiz istek."})
