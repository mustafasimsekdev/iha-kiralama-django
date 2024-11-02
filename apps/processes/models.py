from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from apps.personals.models import Team


# Parça modelini tanımlar, her parça benzersiz bir isimle temsil edilir
class Part(models.Model):
    # Parça ismini saklayan bir karakter alanı; her parça ismi benzersiz (unique) olmalıdır
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.name


# Uçak modelini tanımlar, her uçak benzersiz bir isimle temsil edilir
class Aircraft(models.Model):
    # Uçak ismini saklayan bir karakter alanı; her uçak ismi benzersiz (unique) olmalıdır
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.name


# Parça stoğunu temsil eden model
class PartStock(models.Model):
    # Parça ile ilişkili yabancı anahtar, her parça birden fazla stok kaydına sahip olabilir
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='stocks')
    # Uçağın türü ile ilişkili yabancı anahtar, her uçak türü için ayrı stok kaydı olabilir
    aircraft_type = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='stocks')
    # Takım ile ilişkili yabancı anahtar, her takım kendi parçasını üretebilir ve stoğa ekleyebilir
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    # Stok miktarını temsil eden pozitif tam sayı alanı, varsayılan olarak 0
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.aircraft_type.name} için {self.part.name} ({self.quantity} adet)"

    def increase_stock(self, amount=1):
        """Stok miktarını artırır."""
        self.quantity += amount
        self.save()

    def decrease_stock(self, amount=1):
        """Stok miktarını azaltır. Eğer yeterli stok yoksa hata verir."""
        if self.quantity >= amount:
            self.quantity -= amount
            self.save()
        else:
            raise ValueError(f"{self.part.name} parçasının {self.aircraft_type.name} için yeterli stoku yok!")


# Parça üretim kaydını temsil eden model
class PartProduction(models.Model):
    # Parça ile ilişki, her parça üretim kaydı bir parçaya aittir
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    # Üretimi gerçekleştiren takım ile ilişki
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    # Üretimi gerçekleştiren kişi (User modeli ile ilişki), null olabilir
    producing_personal = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='produced_parts')
    # Üretim tarihi, varsayılan olarak şu anki zamana ayarlanır
    produced_date = models.DateTimeField(default=timezone.now)

    # Parçanın ait olduğu uçak tipi, null ve boş bırakılabilir
    aircraft_type = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True, blank=True, related_name='parts')

    # Geri dönüşüm bilgileri
    recycled_date = models.DateTimeField(null=True, blank=True)
    recycled_personal = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name='recycled_parts')
    # Parçanın montaj durumu
    is_assembled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.part.name} üretildi ({self.produced_date})"

    def produce_part(self, user, part, aircraft_type, quantity=1):
        """Parça üretimini gerçekleştirir ve stoğu artırır."""
        self.producing_personal = user
        self.team = user.personal.team
        self.part = part
        self.aircraft_type = aircraft_type
        self.produced_date = timezone.now()
        self.save()

        # İlgili PartStock kaydını al veya oluştur
        part_stock, created = PartStock.objects.get_or_create(
            part=self.part,
            aircraft_type=self.aircraft_type,
            team=self.team
        )
        # Üretim miktarını stoğa ekle
        part_stock.increase_stock(amount=quantity)

    def recycle_part(self, personal):
        """Belirli bir PartProduction nesnesini geri dönüşüme gönderir ve stoğu azaltır."""
        # Parça montaj edilmişse geri dönüşüm yapılamaz
        if self.is_assembled:
            raise ValueError(f"{self.part.name} zaten montaj yapılmış, geri dönüşüm yapılamaz.")

        # İlgili PartStock kaydını al
        part_stock = PartStock.objects.get(
            part=self.part,
            aircraft_type=self.aircraft_type,
            team=self.team
        )
        # Stoğu azalt
        part_stock.decrease_stock(amount=1)

        # Geri dönüşüm bilgilerini kaydet
        self.recycled_date = timezone.now()
        self.recycled_personal = personal
        self.save()


# Uçak montaj sürecini temsil eden model
class AircraftProduction(models.Model):
    # Montajı yapılan uçak ile ilişki, her montaj işlemi bir uçağa aittir
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    # Montajı gerçekleştiren kullanıcı, null olabilir
    assembly_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Montaj tarihi, varsayılan olarak şu anki zamana ayarlanır
    assembly_date = models.DateTimeField(default=timezone.now)

    def complete_assembly(self, aircraft, assembly_user, used_part_productions):
        """Montaj işlemi: Kullanılan parçaları kaydeder ve stokları günceller."""

        # Montaj işlemi tamamlandığında tarih ve kullanıcı bilgilerini güncelle
        self.aircraft = aircraft
        self.assembly_user = assembly_user
        self.assembly_date = timezone.now()
        self.save()

        # Kullanılan her parçayı montaja ekleyip stokları güncelle
        for part_production in used_part_productions:
            # Parçanın stoğunu azalt
            part_stock = PartStock.objects.get(part=part_production.part, aircraft_type=self.aircraft)
            part_stock.decrease_stock(amount=1)

            # Montaj kaydını oluştur
            PartOfAircraft.objects.create(aircraft_production=self, part_production=part_production)

            # Parçayı montaj edilmiş olarak işaretle
            part_production.is_assembled = True
            part_production.save()

    def __str__(self):
        return f"{self.id}: {self.aircraft.name} - Montaj Tarihi: {self.assembly_date}"


# Uçakta kullanılan parçaları temsil eden model
class PartOfAircraft(models.Model):
    # Uçağın montaj kaydı ile ilişki, her parçanın hangi montaj işleminde kullanıldığını belirtir
    aircraft_production = models.ForeignKey(AircraftProduction, on_delete=models.CASCADE, related_name='parts_used')
    # Kullanılan parça üretim kaydı ile ilişki, parçanın üretim detaylarını belirtir
    part_production = models.ForeignKey(PartProduction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.aircraft_production}: {self.aircraft_production.aircraft.name} - {self.part_production}: {self.part_production.part.name}"
