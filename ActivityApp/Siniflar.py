from datetime import datetime


# Kullanıcı Sınıfı
class Kullanici:
    def __init__(self, ID, kullanici_adi, sifre, email, konum=None, ilgi_alanlari=None,
                 ad=None, soyad=None, dogum_tarihi=None, cinsiyet=None,
                 telefon_numarasi=None, profil_fotografi=None):
        self.__ID = ID
        self.__kullanici_adi = kullanici_adi
        self.__sifre = sifre
        self.__email = email
        self.__konum = konum
        self.__ilgi_alanlari = ilgi_alanlari
        self.__ad = ad
        self.__soyad = soyad
        self.__dogum_tarihi = dogum_tarihi
        self.__cinsiyet = cinsiyet
        self.__telefon_numarasi = telefon_numarasi
        self.__profil_fotografi = profil_fotografi

    # ID
    def get_ID(self):
        return self.__ID

    def set_ID(self, ID):
        self.__ID = ID

    # Kullanıcı Adı
    def get_kullanici_adi(self):
        return self.__kullanici_adi

    def set_kullanici_adi(self, kullanici_adi):
        self.__kullanici_adi = kullanici_adi

    # Şifre
    def get_sifre(self):
        return self.__sifre

    def set_sifre(self, sifre):
        self.__sifre = sifre

    # E-posta
    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    # Konum
    def get_konum(self):
        return self.__konum

    def set_konum(self, konum):
        self.__konum = konum

    # İlgi Alanları
    def get_ilgi_alanlari(self):
        return self.__ilgi_alanlari

    def set_ilgi_alanlari(self, ilgi_alanlari):
        self.__ilgi_alanlari = ilgi_alanlari

    # Ad
    def get_ad(self):
        return self.__ad

    def set_ad(self, ad):
        self.__ad = ad

    # Soyad
    def get_soyad(self):
        return self.__soyad

    def set_soyad(self, soyad):
        self.__soyad = soyad

    # Doğum Tarihi
    def get_dogum_tarihi(self):
        return self.__dogum_tarihi

    def set_dogum_tarihi(self, dogum_tarihi):
        self.__dogum_tarihi = dogum_tarihi

    # Cinsiyet
    def get_cinsiyet(self):
        return self.__cinsiyet

    def set_cinsiyet(self, cinsiyet):
        self.__cinsiyet = cinsiyet

    # Telefon Numarası
    def get_telefon_numarasi(self):
        return self.__telefon_numarasi

    def set_telefon_numarasi(self, telefon_numarasi):
        self.__telefon_numarasi = telefon_numarasi

    # Profil Fotoğrafı
    def get_profil_fotografi(self):
        return self.__profil_fotografi

    def set_profil_fotografi(self, profil_fotografi):
        self.__profil_fotografi = profil_fotografi

    # Print ile bilgileri yazdırmayı sağlaycak fonksiyon
    def __str__(self):
        return (
            f"Kullanıcı Bilgileri:\n"
            f"ID: {self.get_ID()}\n"
            f"Kullanıcı Adı: {self.get_kullanici_adi()}\n"
            f"Email: {self.get_email()}\n"
            f"Konum: {self.get_konum()}\n"
            f"İlgi Alanları: {self.__ilgi_alanlari.replace(',', ', ')}\n"  # Daha okunaklı olsun diye
            f"Ad: {self.get_ad()}\n"
            f"Soyad: {self.get_soyad()}\n"
            f"Doğum Tarihi: {self.get_dogum_tarihi()}\n"
            f"Cinsiyet: {self.get_cinsiyet()}\n"
            f"Telefon Numarası: {self.get_telefon_numarasi()}\n"
            f"Profil Fotoğrafı: {self.get_profil_fotografi()}"
        )


# Etkinlik Sınıfı
class Etkinlik:
    def __init__(self, ID, etkinlik_adi, aciklama=None, tarih=None, saat=None,
                 etkinlik_suresi=None, konum=None, kategori=None, etkinlik_fotografi=None):
        self.__ID = ID
        self.__etkinlik_adi = etkinlik_adi
        self.__aciklama = aciklama
        self.__tarih = tarih
        self.__saat = saat
        self.__etkinlik_suresi = etkinlik_suresi
        self.__konum = konum
        self.__kategori = kategori
        self.__etkinlik_fotografi = etkinlik_fotografi

    # ID
    def get_ID(self):
        return self.__ID

    def set_ID(self, ID):
        self.__ID = ID

    # Etkinlik Adı
    def get_etkinlik_adi(self):
        return self.__etkinlik_adi

    def set_etkinlik_adi(self, etkinlik_adi):
        self.__etkinlik_adi = etkinlik_adi

    # Açıklama
    def get_aciklama(self):
        return self.__aciklama

    def set_aciklama(self, aciklama):
        self.__aciklama = aciklama

    # Tarih
    def get_tarih(self):
        return self.__tarih

    def set_tarih(self, tarih):
        self.__tarih = tarih

    # Saat
    def get_saat(self):
        return self.__saat

    def set_saat(self, saat):
        self.__saat = saat

    # Etkinlik Süresi
    def get_etkinlik_suresi(self):
        return self.__etkinlik_suresi

    def set_etkinlik_suresi(self, etkinlik_suresi):
        self.__etkinlik_suresi = etkinlik_suresi

    # Konum
    def get_konum(self):
        return self.__konum

    def set_konum(self, konum):
        self.__konum = konum

    # Kategori
    def get_kategori(self):
        return self.__kategori

    def set_kategori(self, kategori):
        self.__kategori = kategori

    # Etkinlik Fotoğrafı
    def get_etkinlik_fotografi(self):
        return self.__etkinlik_fotografi

    def set_etkinlik_fotografi(self, etkinlik_fotografi):
        self.__etkinlik_fotografi = etkinlik_fotografi

    # Print ile bilgileri yazdırmayı sağlayacak fonksiyon
    def __str__(self):
        return (
            f"Etkinlik Bilgileri:\n"
            f"ID: {self.get_ID()}\n"
            f"Etkinlik Adı: {self.get_etkinlik_adi()}\n"
            f"Açıklama: {self.get_aciklama() or 'Belirtilmemiş'}\n"  # Boşsa varsayılan metin
            f"Tarih: {self.get_tarih() or 'Belirtilmemiş'}\n"
            f"Saat: {self.get_saat() or 'Belirtilmemiş'}\n"
            f"Etkinlik Süresi: {self.get_etkinlik_suresi() or 'Belirtilmemiş'}\n"
            f"Konum: {self.get_konum() or 'Belirtilmemiş'}\n"
            f"Kategori: {self.get_kategori() or 'Belirtilmemiş'}"
        )


# Etkinlik Onay Sınıfı
class EtkinlikOnay:
    def __init__(self, onay: False, etkinlik_id):
        self.__onay = onay
        self.__etkinlik_id = etkinlik_id

    # Onay
    def get_onay(self):
        return self.__onay

    def set_onay(self, onay):
        self.__onay = onay

    # Etkinlik ID
    def get_etkinlik_id(self):
        return self.__etkinlik_id

    def set_etkinlik_id(self, etkinlik_id):
        self.__etkinlik_id = etkinlik_id


# Katılımcı Sınıfı
class Katilimci:
    def __init__(self, kullanici_id, etkinlik_id):
        self.__kullanici_id = kullanici_id
        self.__etkinlik_id = etkinlik_id

    # Kullanıcı ID
    def get_kullanici_id(self):
        return self.__kullanici_id

    def set_kullanici_id(self, kullanici_id):
        self.__kullanici_id = kullanici_id

    # Etkinlik ID
    def get_etkinlik_id(self):
        return self.__etkinlik_id

    def set_etkinlik_id(self, etkinlik_id):
        self.__etkinlik_id = etkinlik_id


# Olusturan Sınıfı
class Olusturan:
    def __init__(self, kullanici_id, etkinlik_id):
        self.__kullanici_id = kullanici_id
        self.__etkinlik_id = etkinlik_id

    # Kullanıcı ID
    def get_kullanici_id(self):
        return self.__kullanici_id

    def set_kullanici_id(self, kullanici_id):
        self.__kullanici_id = kullanici_id

    # Etkinlik ID
    def get_etkinlik_id(self):
        return self.__etkinlik_id

    def set_etkinlik_id(self, etkinlik_id):
        self.__etkinlik_id = etkinlik_id


# Mesaj Sınıfı
class Mesaj:
    def __init__(self, mesaj_id, gonderici_id, alici_id, mesaj_metni, gonderim_zamani=None):
        self.__mesaj_id = mesaj_id
        self.__gonderici_id = gonderici_id
        self.__alici_id = alici_id
        self.__mesaj_metni = mesaj_metni
        self.__gonderim_zamani = gonderim_zamani if gonderim_zamani else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Mesaj ID
    def get_mesaj_id(self):
        return self.__mesaj_id

    def set_mesaj_id(self, mesaj_id):
        self.__mesaj_id = mesaj_id

    # Gönderici ID
    def get_gonderici_id(self):
        return self.__gonderici_id

    def set_gonderici_id(self, gonderici_id):
        self.__gonderici_id = gonderici_id

    # Alıcı ID
    def get_alici_id(self):
        return self.__alici_id

    def set_alici_id(self, alici_id):
        self.__alici_id = alici_id

    # Mesaj Metni
    def get_mesaj_metni(self):
        return self.__mesaj_metni

    def set_mesaj_metni(self, mesaj_metni):
        self.__mesaj_metni = mesaj_metni

    # Gönderim Zamanı
    def get_gonderim_zamani(self):
        return self.__gonderim_zamani

    def set_gonderim_zamani(self, gonderim_zamani):
        self.__gonderim_zamani = gonderim_zamani


# Puan Sınıfı
class Puan:
    def __init__(self, kullanici_id, etkinlik_id, puan, kazanilan_tarih=None):
        self.__kullanici_id = kullanici_id
        self.__etkinlik_id = etkinlik_id
        self.__puan = puan
        self.__kazanilan_tarih = kazanilan_tarih if kazanilan_tarih else datetime.now().strftime("%Y-%m-%d")

    # Kullanıcı ID
    def get_kullanici_id(self):
        return self.__kullanici_id

    def set_kullanici_id(self, kullanici_id):
        self.__kullanici_id = kullanici_id

    # Etkinlik ID
    def get_etkinlik_id(self):
        return self.__etkinlik_id

    def set_etkinlik_id(self, etkinlik_id):
        self.__etkinlik_id = etkinlik_id

    # Puan
    def get_puan(self):
        return self.__puan

    def set_puan(self, puan):
        self.__puan = puan

    # Kazanılan Tarih
    def get_kazanilan_tarih(self):
        return self.__kazanilan_tarih

    def set_kazanilan_tarih(self, kazanilan_tarih):
        self.__kazanilan_tarih = kazanilan_tarih
