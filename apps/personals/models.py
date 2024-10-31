from django.db import models
from django.contrib.auth.models import User, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


# Team model representing different teams like Kanat Takımı, Gövde Takımı, etc.
class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        db_table = 'teams'  # Custom table name

    def __str__(self):
        return self.name


# User modeline özel CustomUserManager tanımlıyoruz
class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, team, password=None):
        if not email and not username:
            raise ValueError('Users must have both an email address and username')

        # Create or get the User instance
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': self.normalize_email(email),
                'is_staff': True,
            }
        )

        if created:  # Only set password and create Personnel if the user is newly created
            user.set_password(password)
            user.save(using=self._db)
            Personal.objects.get_or_create(user=user, team=Team.objects.get(name=team))  # Ensure Personnel is created

        return user

    def create_superuser(self, username, first_name, last_name, email, team=None, password=None):
        if not email and not username:
            raise ValueError('Users must have both an email address and username')

        # Get or create user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': self.normalize_email(email),
                'is_staff': True,
                'is_superuser': True,  # Set superuser defaults here
            }
        )

        if created:  # Only set password if the user is newly created
            user.set_password(password)
            user.save(using=self._db)
            if team:
                Personal.objects.get_or_create(user=user, team=Team.objects.get(name=team))

        return user


# Personal modelini User modeli ile ilişkilendiriyoruz
class Personal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='personals')

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        db_table = 'personal_team'

    def __str__(self):
        return f"{self.user.email} - {self.team.name}"

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created and hasattr(instance, 'personal'):
            Personal.objects.create(user=instance)


# User modeline CustomUserManager ataması
User.add_to_class('objects', CustomUserManager())
