from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.personals.models import Team
from .models import Part, Aircraft


@receiver(post_migrate)
def create_default_parts_for_existing_teams(sender, **kwargs):
    if sender.name == 'apps.processes':  # Ensures it only runs for your app
        teams_without_montaj = ["Kanat", "Gövde", "Kuyruk", "Aviyonik"]

        for name in teams_without_montaj:
            # Team kaydını kontrol et
            team = Team.objects.filter(name=name).first()

            if team:
                # Eğer takım varsa ve Part yoksa, o takıma özel bir Part oluştur
                Part.objects.get_or_create(name=team.name)


@receiver(post_migrate)
def create_default_parts_for_existing_teams(sender, **kwargs):
    if sender.name == 'apps.processes':  # Ensures it only runs for your app
        aircraft = ["TB2", "TB3", "AKINCI", "KIZILELMA"]

        for a_name in aircraft:
            # Ucak olustur veya olusturma
            Aircraft.objects.get_or_create(name=a_name)