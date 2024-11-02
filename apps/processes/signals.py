from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.personals.models import Team
from .models import Part, Aircraft

# Migrasyon işlemleri tamamlandığında belirli takımlar için varsayılan parçaları oluşturur
@receiver(post_migrate)
def create_default_parts_for_existing_teams(sender, **kwargs):
    # Bu fonksiyonun sadece 'apps.processes' uygulaması için çalışmasını sağlar
    if sender.name == 'apps.processes':
        # Montaj takımı haricindeki takımların listesi
        teams_without_montaj = ["Kanat", "Gövde", "Kuyruk", "Aviyonik"]

        for name in teams_without_montaj:
            # Team kaydını kontrol et
            team = Team.objects.filter(name=name).first()

            # Eğer takım mevcutsa, o takım için bir 'Part' kaydı oluşturulmamışsa oluşturur
            if team:
                Part.objects.get_or_create(name=team.name)


@receiver(post_migrate)
def create_default_aircraft_for_existing_teams(sender, **kwargs):
    if sender.name == 'apps.processes':
        # Varsayılan olarak oluşturulacak uçakların listesi
        aircraft = ["TB2", "TB3", "AKINCI", "KIZILELMA"]

        for a_name in aircraft:
            # İlgili uçak adıyla kayıtlı bir Aircraft kaydı varsa alır, yoksa yeni bir kayıt oluşturur
            Aircraft.objects.get_or_create(name=a_name)