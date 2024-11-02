### İHA Kiralama Projesi - README

Bu proje, İHA (İnsansız Hava Aracı) kiralama ve üretim yönetimi için geliştirilmiş bir platformdur. Django kullanılarak geliştirilmiştir ve personel, parça, takım ve uçak üretim süreçlerini yönetmeyi sağlar. Projede takım bazlı parça üretimi, envanter kontrolü, montaj işlemleri ve eksik parça uyarıları gibi özellikler bulunmaktadır.

---

### Proje İçeriği

1. **Django Tabanlı Backend**
   - İHA kiralama ve üretim süreci için modüler bir yapı sunar.
   - `apps.personals`: Personel ve takım yönetimi.
   - `apps.processes`: Parça üretimi ve montaj işlemleri.
   - `apps.dashboards`: Gösterge tabloları ve raporlamalar.
   - `apps.pages`: Kullanıcı bilgilerini değiştirme işemleri (Bu bitmedi).
   - `authentication`: Kullanıcı kimlik doğrulama işlemleri.

2. **Özellikler**
   - **Parça Üretimi**: Her takım kendi parçalarını üretir ve envanterde stoklar.
   - **Montaj**: Montaj takımı gerekli tüm parçaları toplayarak uçak montajını gerçekleştirir.
   - **Envanter Yönetimi**: Eksik parçalar için uyarılar verilir ve stoklar takip edilir.
   - **Kullanıcı Yetkilendirme**: Her kullanıcının takım bazında belirli yetkileri vardır.
   - **Varsayılan Veriler**: Signals ile bazı varsayılan veriler (takımlar, parçalar ve kullanıcılar) otomatik olarak veritabanına eklenir.
   - **Listeleme ve Filtreleme**: Parça ve uçakların detaylı listelenmesi için DataTable kullanılmıştır. 
   - **AJAX Desteği**: HTML şablonlarında POST ve GET işlemleri için AJAX kullanılmıştır.
---

### Projeyi Çalıştırmak İçin Adımlar

#### 1. Gerekli Paketleri Kurma

Öncelikle projenin gereksinimlerini yüklemeniz gerekir. `requirements.txt` dosyasındaki bağımlılıkları yüklemek için aşağıdaki komutu kullanın:

```bash
pip install -r requirements.txt
```

> **Not:** Gereksinimlerdeki bazı önemli paketler şunlardır:
> - `Django==5.1.2`
> - `djangorestframework==3.15.2`
> - `psycopg2==2.9.10` (PostgreSQL veritabanı bağlantısı için)
> - `python-dotenv==1.0.1` (Çevre değişkenlerini `.env` dosyasından yüklemek için)

#### 2. Çevre Değişkenleri Dosyasını (.env) Ayarlama

Proje, çevre değişkenlerini kullanarak çalışır. Proje kök dizininde `.env` dosyasını oluşturun ve aşağıdaki gibi doldurun:

```plaintext
DEBUG=True
DJANGO_ENVIRONMENT="local"
SECRET_KEY="proje-icin-gizli-anahtar"
BASE_URL="http://127.0.0.1:8000"

# Veritabanı bilgileri
DB_ENGINE="django.db.backends.postgresql"
DB_NAME="iha_kiralama_db"
DB_USER="postgres"
DB_PASSWORD="parolanız"
DB_HOST="localhost"
DB_PORT="5432"
```

> **Not:** Üretim ortamında `DEBUG=False` yapmayı unutmayın ve `.env` dosyasını gizli tutun.

#### 3. Veritabanı Ayarları

Veritabanı işlemlerini gerçekleştirmek için aşağıdaki komutları kullanarak veritabanını oluşturun ve migrations işlemlerini uygulayın:

```bash
python manage.py makemigrations
python manage.py migrate
```

Bu işlemler, veritabanı tablolarınızı oluşturur.

#### 4. Varsayılan Verilerin Eklenmesi

Signals kullanılarak projeye özgü varsayılan veriler veritabanına otomatik olarak eklenir. Bu veriler:
   - Takımlar (Kanat, Gövde, Kuyruk, Aviyonik, Montaj)
   - Parçalar ve uçak türleri (TB2, TB3, AKINCI, KIZILELMA)
   - Varsayılan kullanıcılar

#### 5. Giriş Yapmak İçin Varsayılan Kullanıcılar

Projeye dahil olan varsayılan kullanıcılar, login sayfasında test amaçlı kullanılabilir. Örneğin:
   - **E-mail**: `simsekkanat@baykartech.com`, **Şifre**: `Ihakanat.123`
   - **E-mail**: `simsekgovde@baykartech.com`, **Şifre**: `Ihagovde.123`
   - **E-mail**: `simsekkuyruk@baykartech.com`, **Şifre**: `Ihakuyruk.123`
   - **E-mail**: `simsekaviyonik@baykartech.com`, **Şifre**: `Ihaaviyonik.123`
   - **E-mail**: `simsekmontaj@baykartech.com`, **Şifre**: `Ihamontaj.123`

> **Not:** Admin kullanıcısı için:
> - **E-mail**: `simsekadmin@baykartech.com`, **Şifre**: `Ihaadmin.123`

#### 6. Geliştirme Sunucusunu Başlatma

Proje geliştirme ortamında çalıştırılabilir. Aşağıdaki komutu kullanarak sunucuyu başlatın:

```bash
python manage.py runserver
```

Sunucuyu başlattıktan sonra projeyi [http://127.0.0.1:8000](http://127.0.0.1:8000) adresinden görüntüleyebilirsiniz.

---

### Önemli Notlar

- **Signal İşlemleri**: Signals dosyaları, varsayılan verilerin veritabanına otomatik eklenmesi için kullanılır. Bu işlemler `post_migrate` sinyali ile tetiklenir.
- **Kullanıcı Yetkilendirmeleri**: Her takım sadece kendi parçasını üretebilir. Montaj işlemleri için montaj takımının yetkisi bulunmaktadır.
- **Dil Ayarları**: Proje çoklu dil desteğine sahiptir. Varsayılan dil `Türkçe` olarak ayarlanmıştır.

---

### Proje Yapısı

```plaintext
iha_kiralama/
├── apps/
│   ├── personals/         # Personel ve Takım yönetimi
│   ├── processes/         # Parça üretimi ve montaj işlemleri
│   ├── dashboards/        # Gösterge tabloları ve raporlar
│   └── pages/             # Ekstra sayfalar
├── authentication/        # Kullanıcı kimlik doğrulama işlemleri
├── config/                # Proje ayarları ve yapılandırma
├── templates/             # HTML şablonları
├── src/                # Statik dosyalar (CSS, JS, img)
├── manage.py              # Django yönetim aracı
└── .env                   # Çevre değişkenleri dosyası
```

---

### Gereksinimler

Bu proje için Python 3.8+ sürümü ve aşağıdaki paketler gereklidir (hepsi `requirements.txt` dosyasında listelenmiştir):

- Django==5.1.2
- djangorestframework==3.15.2
- psycopg2==2.9.10
- python-dotenv==1.0.1
- whitenoise==6.7.0

Tüm gereksinimleri `pip install -r requirements.txt` komutu ile yükleyebilirsiniz.

---

### Proje Geliştiricisi Hakkında

Bu proje, Mustafa Şimşek tarafından geliştirilmiştir. Aşağıda geliştirici ile ilgili bilgilere ve iletişim bilgilerine ulaşabilirsiniz.

#### Mustafa Şimşek
- **Meslek**: Yazılım Geliştirici
- **Uzmanlık Alanları**: Python, Doğal Dil İşleme, Derin/Makine Öğrenmesi, Django, REST API, Veri Tabanı Yönetimi, Algoritma Geliştirme
- **GitHub**: [@mustafasimsekdev](https://github.com/mustafasimsekdev)
- **LinkedIn**: [linkedin.com/in/mustafasimsekdev](https://www.linkedin.com/in/mustafasimsekdev)
- **Twitter**: [@mustafasimsekpy](https://x.com/mustafasimsekpy)

Geliştirici hakkında daha fazla bilgi edinmek için yukarıdaki bağlantılardan ulaşabilirsiniz. Proje hakkında sorularınız veya geri bildirimleriniz için Mustafa Şimşek'e ulaşabilirsiniz. 

---

### Proje Bağlantıları

Projeyi GitHub üzerinden görmek için [bu bağlantıyı](https://github.com/mustafasimsekdev/iha-kiralama-django) kullanabilirsiniz.

---

### Lisans

Bu proje, [MIT Lisansı](https://opensource.org/licenses/MIT) ile lisanslanmıştır.