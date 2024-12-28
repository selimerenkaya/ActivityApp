import re  # Kullanıcı girişi sırasında kontrole yardım ediyo
import requests
import random
from datetime import datetime


# Register değişkenleri için kontrol fonksiyonu
def control_RegisterData(username, password, email, location, interest, name, surname, birthday, gender, telephone):
    errors = []

    # Kullanıcı adı kontrolü (3-20 karakter, alfanumerik)
    pattern = r"^[a-zA-Z0-9çşğüöıÇŞĞÜÖİ]{3,20}$"
    if not re.match(pattern, username, re.UNICODE):
        errors.append("Kullanıcı adı 3-20 karakter arasında ve alfanumerik olmalıdır.")

    # Şifre kontrolü (8-24 karakter, en az bir büyük harf, bir sayı ve Türkçe harf desteği)
    pattern = r"^(?=.*[A-ZÇŞĞÜÖİ])(?=.*\d)[A-Za-zÇŞĞÜÖİçşğüöı\d@$!%*?&_]{8,24}$"
    if not re.match(pattern, password, re.UNICODE):
        errors.append("Şifre 8-24 karakter arasında, en az bir büyük harf, bir sayı "
                      "ve izin verilen özel karakterlerden biri içermelidir.")

    # E-posta kontrolü
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        errors.append("Geçerli bir e-posta adresi giriniz.")

    # Telefon numarası kontrolü (10 haneli Türk numarası örneği)
    if not re.match(r"^05\d{9}$", telephone):
        errors.append("Geçerli bir Türk telefon numarası giriniz (05XXXXXXXXX).")

    # Doğum tarihi kontrolü (YYYY-MM-DD)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", birthday):
        errors.append("Doğum tarihi YYYY-MM-DD formatında olmalıdır.")

    # Cinsiyet kontrolü (Belirli seçenekler)
    if gender not in ['Erkek', 'Kadın']:
        errors.append("Cinsiyet seçimi geçersiz.")

    # İsim ve soyisim kontrolü (sadece harf, min 2 karakter)
    if not re.match(r"^[a-zA-ZğüşıöçĞÜŞİÖÇ]{2,}$", name):
        errors.append("İsim sadece harflerden oluşmalı ve en az 2 karakter olmalıdır.")
    if not re.match(r"^[a-zA-ZğüşıöçĞÜŞİÖÇ]{2,}$", surname):
        errors.append("Soyisim sadece harflerden oluşmalı ve en az 2 karakter olmalıdır.")

    # Lokasyon ve ilgi alanları boş olmamalı
    if not location.strip():
        errors.append("Lokasyon boş bırakılamaz.")
    if not interest.strip():
        errors.append("İlgi alanı boş bırakılamaz.")

    return errors


# Login değişkenleri için kontrol fonksiyonu
def control_LoginData(username, password):
    errors = []
    # Kullanıcı adı kontrolü (3-20 karakter, alfanumerik)
    pattern = r"^[a-zA-Z0-9çşğüöıÇŞĞÜÖİ]{3,20}$"
    if not re.match(pattern, username, re.UNICODE):
        errors.append("Kullanıcı adı 3-20 karakter arasında ve alfanumerik olmalıdır.")

    # Şifre kontrolü (8-24 karakter, en az bir büyük harf, bir sayı ve Türkçe harf desteği)
    pattern = r"^(?=.*[A-ZÇŞĞÜÖİ])(?=.*\d)[A-Za-zÇŞĞÜÖİçşğüöı\d@$!%*?&_]{8,24}$"
    if not re.match(pattern, password, re.UNICODE):
        errors.append("Şifre 8-24 karakter arasında, en az bir büyük harf, bir sayı "
                      "ve izin verilen özel karakterlerden biri içermelidir.")

    return errors


# Password değişkenleri için kontrol fonksiyonu
def control_PasswordData(username, email, name, surname, birthday, telephone, password):
    errors = []
    # Kullanıcı adı kontrolü (3-20 karakter, alfanumerik)
    pattern = r"^[a-zA-Z0-9çşğüöıÇŞĞÜÖİ]{3,20}$"
    if not re.match(pattern, username, re.UNICODE):
        errors.append("Kullanıcı adı 3-20 karakter arasında ve alfanumerik olmalıdır.")

    # Şifre kontrolü (8-24 karakter, en az bir büyük harf, bir sayı ve Türkçe harf desteği)
    pattern = r"^(?=.*[A-ZÇŞĞÜÖİ])(?=.*\d)[A-Za-zÇŞĞÜÖİçşğüöı\d@$!%*?&_]{8,24}$"
    if not re.match(pattern, password, re.UNICODE):
        errors.append("Şifre 8-24 karakter arasında, en az bir büyük harf, bir sayı "
                      "ve izin verilen özel karakterlerden biri içermelidir.")

    # E-posta kontrolü
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        errors.append("Geçerli bir e-posta adresi giriniz.")

    # Telefon numarası kontrolü (10 haneli Türk numarası örneği)
    if not re.match(r"^05\d{9}$", telephone):
        errors.append("Geçerli bir Türk telefon numarası giriniz (05XXXXXXXXX).")

    # Doğum tarihi kontrolü (YYYY-MM-DD)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", birthday):
        errors.append("Doğum tarihi YYYY-MM-DD formatında olmalıdır.")


    # İsim ve soyisim kontrolü (sadece harf, min 2 karakter)
    if not re.match(r"^[a-zA-ZğüşıöçĞÜŞİÖÇ]{2,}$", name):
        errors.append("İsim sadece harflerden oluşmalı ve en az 2 karakter olmalıdır.")
    if not re.match(r"^[a-zA-ZğüşıöçĞÜŞİÖÇ]{2,}$", surname):
        errors.append("Soyisim sadece harflerden oluşmalı ve en az 2 karakter olmalıdır.")

    return errors


# İlgi alanına bağlı olarak rastgele etknilik kategroisi döndüren fonksyion
def ilgi_alani_kategorisi(ilgi_alani, kategoriler):   # BUNUN İÇİN TABLO EKLENECEK BİR SÜRÜ
    return random.choice(kategoriler.get(ilgi_alani, ["Genel Etkinlik"]))


# Yaş hesaplamaya yarar
# Sadece kullanıcı için çalışır
def hesaplaYas(dogum_tarihi):
    # Tarihi listeye dönüştürür
    birth_date = dogum_tarihi.split("-")

    # Bugünün tarihini al
    today = datetime.today()

    # Yaşı hesapla
    age = today.year - int(birth_date[0])

    # Ay ve gün karşılaştırmasıyla düzeltme yap
    if (today.month, today.day) < (int(birth_date[1]), int(birth_date[2])):
        age -= 1

    return age


# Kullanıcı konumuna göre etkinlik listesini mesafelerine göre sıralar.
def etkinlikSiralaUzaklik(user_location_name, events):
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    
    # Etkinlik konumlarını çıkar
    event_locations = [event.get_konum() for event in events]
    
    # Hedefleri böl (15'den fazla hedef olamaz)
    chunk_size = 25
    event_chunks = [event_locations[i:i + chunk_size] for i in range(0, len(event_locations), chunk_size)]
    
    results = []

    for chunk in event_chunks:
        destinations = "|".join(chunk)
        response = requests.get(
            base_url,
            params={
                "origins": user_location_name,
                "destinations": destinations,
                "key": "AIzaSyDaZl18l0BX8viIEr7A3dKUK03aXuJ-fwE",  # API anahtarınız
                "units": "metric",
            },
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Eğer `rows` boş ise bir hata gösterin
            if not data["rows"] or not data["rows"][0]["elements"]:
                raise Exception(f"API, boş sonuç döndürdü: {data}")
            
            for event, element in zip(events, data["rows"][0]["elements"]):
                if element["status"] == "OK":
                    results.append(
                        {
                            "event": event,
                            "distance": element["distance"]["value"],  # Metre
                            "duration": element["duration"]["value"],  # Saniye
                        }
                    )
                else:
                    print(f"Hata: {event.get_konum()} için geçerli mesafe bilgisi yok. Status: {element['status']}")
        else:
            raise Exception(f"API Hatası: {response.status_code} - {response.text}")
    
    # Mesafeye göre sırala
    results.sort(key=lambda x: x["distance"])
    
    # Sadece sıralanmış etkinlik nesnelerini döndür
    return [result["event"] for result in results]



# Günümüzden sonraki etkinlikleri döndürür
def etkinliklerGelecek(events):
    bugun = datetime.now()
    oneri_listesi = []

    for event in events:
        try:
            etkinlik_tarihi = datetime.strptime(event.get_tarih(), "%Y-%m-%d")
            if etkinlik_tarihi > bugun:
                oneri_listesi.append(event)
        except ValueError:
            print(f"Hata: {event['ad']} etkinliğinin tarihi geçersiz ({event.get_tarih()}).")

    return oneri_listesi
