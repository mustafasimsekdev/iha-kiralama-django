from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Team
from django.contrib.auth.models import User


@receiver(post_migrate)
def create_default_teams(sender, **kwargs):
    if sender.name == 'personals':  # Ensures it only runs for your app
        teams = ["Kanat", "Gövde", "Kuyruk", "Aviyonik", "Montaj"]
        for team_name in teams:
            Team.objects.get_or_create(name=team_name)


@receiver(post_migrate)
def create_default_personals(sender, **kwargs):
    if sender.name == 'personals':  # Ensures it only runs for your app
        personals = [
            {'username': 'simsekkanat', 'first_name': 'Kanat', 'last_name': 'Simsek',
             'email': 'simsekkanat@baykartech.com', 'password': 'Ihakanat.123', 'team': 'Kanat'},
            {'username': 'simsekgovde', 'first_name': 'Govde', 'last_name': 'Simsek',
             'email': 'simsekgovde@baykartech.com', 'password': 'Ihagovde.123', 'team': 'Gövde'},
            {'username': 'simsekkuyruk', 'first_name': 'Kuyruk', 'last_name': 'Simsek',
             'email': 'simsekkuyruk@baykartech.com', 'password': 'Ihakuyruk.123', 'team': 'Kuyruk'},
            {'username': 'simsekaviyonik', 'first_name': 'Aviyonik', 'last_name': 'Simsek',
             'email': 'simsekaviyonik@baykartech.com', 'password': 'Ihaaviyonik.123', 'team': 'Aviyonik'},
            {'username': 'simsekmontaj', 'first_name': 'Montaj', 'last_name': 'Simsek',
             'email': 'simsekmontaj@baykartech.com', 'password': 'Ihamontaj.123', 'team': 'Montaj'},
        ]

        for personal in personals:
            User.objects.create_user(username=personal['username'], first_name=personal['first_name'],
                                     last_name=personal['last_name'], email=personal['email'],
                                     password=personal['password'], team=personal['team'])

        super_user = {'username': 'simsekadmin', 'first_name': 'Admin', 'last_name': 'Simsek',
                      'email': 'simsekadmin@baykartech.com', 'password': 'Ihaadmin.123'}
        User.objects.create_superuser(username=super_user['username'], first_name=super_user['first_name'],
                                      last_name=super_user['last_name'], email=super_user['email'],
                                      password=super_user['password'])
