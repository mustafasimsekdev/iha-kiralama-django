from django.db import models
from django.contrib.auth.models import User, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


# Takımları temsil eden model (örneğin, Kanat Takımı, Gövde Takımı gibi)
class Team(models.Model):
    # Takımın ismini temsil eden bir karakter alanı. Her takım ismi benzersiz (unique) olmalıdır.
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        # Bu modelin veritabanında saklanacağı tablo ismini belirler.
        db_table = 'teams'

    def __str__(self):
        return self.name


# User modeline özel CustomUserManager tanımlıyoruz
class CustomUserManager(BaseUserManager):
    # Standart kullanıcı oluşturan bir metot
    def create_user(self, username, first_name, last_name, email, team, password=None):
        if not email and not username:
            raise ValueError('Users must have both an email address and username')

        # Kullanıcıyı yarat veya getir. Eğer kullanıcı mevcut değilse, belirtilen varsayılanlarla yaratılır.
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': self.normalize_email(email),
                'is_staff': True,
            }
        )

        # Yeni bir kullanıcı yaratıldıysa şifre ayarla ve kaydet
        if created:
            user.set_password(password)
            user.save(using=self._db)
            # Kullanıcının personel kaydını oluştur ve belirtilen takımı ata
            Personal.objects.get_or_create(user=user, team=Team.objects.get(name=team))  # Ensure Personnel is created

        return user

    # Superuser (yönetici) oluşturan bir metot
    def create_superuser(self, username, first_name, last_name, email, team=None, password=None):
        if not email and not username:
            raise ValueError('Users must have both an email address and username')

        # Superuser'ı yarat veya getir. Eğer kullanıcı mevcut değilse, belirtilen varsayılanlarla yaratılır.
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

        # Yeni bir superuser yaratıldıysa şifre ayarla ve kaydet
        if created:
            user.set_password(password)
            user.save(using=self._db)
            # Eğer bir takım belirtilmişse, personel kaydını oluştur ve takımı ata
            if team:
                Personal.objects.get_or_create(user=user, team=Team.objects.get(name=team))

        return user


# Personal modelini User modeli ile ilişkilendiriyoruz
class Personal(models.Model):
    # Her Personal kaydını bir User kaydıyla birebir (OneToOne) ilişkilendirir.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal')
    # Her Personal kaydını bir Team kaydıyla ilişkilendirir. Bir takımda birden fazla personel olabilir.
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='personals')

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        # Bu modelin veritabanında saklanacağı tablo ismini belirler.
        db_table = 'personal_team'

    def __str__(self):
        return f"{self.user.email} - {self.team.name}"

    # User kaydı oluşturulduğunda otomatik olarak bir Personal kaydı oluşturmak için bir sinyal.
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        # Eğer yeni bir User kaydı oluşturulmuşsa ve henüz Personal kaydı yoksa
        if created and hasattr(instance, 'personal'):
            Personal.objects.create(user=instance)


# User modeline CustomUserManager ataması
User.add_to_class('objects', CustomUserManager())
