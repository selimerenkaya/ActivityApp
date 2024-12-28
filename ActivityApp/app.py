from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file, flash
import io
import Database
import Siniflar
import Fonksiyonlar
import os
import locale
from datetime import datetime

# Türkçe diline uygun sıralama ayarları
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
app = Flask(__name__)
app.secret_key = "secretkey"  # Güvenlik için bir anahtar


# Giriş yapmayan kullanıcıların karşılacağı ana sayfa
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('home.html')


# Giriş ve Kayıt sayfası
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        ilgi_alanlari = Database.getAllIlgiAlanlari()
        interests: list = list()
        for ilgi in ilgi_alanlari:
            interests.append(ilgi[0])
        hazir_konumlar = Database.getAllKonumlar()
        if hazir_konumlar:
            hazir_konumlar = [konum[0] for konum in hazir_konumlar]
        else:
            hazir_konumlar = []
        if hazir_konumlar:
            hazir_konumlar = sorted(hazir_konumlar, key=locale.strxfrm)
        return render_template('login.html', ilgi_alanlar=interests, hazir_konumlar=hazir_konumlar)

    elif request.method == 'POST':
        try:
            action = request.form.get('action')  # Login mi Register mı Password mu bilgisi
            if action == "login":
                # Giriş yaparken sadece bu bilgilerin çekilmesi yeterli
                username = request.form.get('username_login')
                password = request.form.get('password_login')

                # Format hatalıysa exception
                errors = Fonksiyonlar.control_LoginData(username, password)
                if errors:
                    raise Exception(errors[0])

                # Kullanıcı bilgilerini çeker
                result = Database.searchKullanici_ByUsername(username)
                if not result:
                    raise Exception("Kullanıcı adı veya şifre yanlış.")
                else:
                    stores_password = result[2]
                    if password == stores_password:  # Şifre kontrol
                        session['username'] = username
                        print(session['username'])
                        return redirect(url_for('user_anasayfa'))
                    else:
                        raise Exception("Kullanıcı adı veya şifre yanlış.")

            elif action == "password":
                username = request.form.get('username_password')
                email = request.form.get('email_password')
                name = request.form.get('name_password')
                surname = request.form.get('surname_password')
                birthday = request.form.get('birthday_password')
                telephone = request.form.get('telephone_password')
                password = request.form.get('password_password')

                # Bilgilerin formatını kontrol edip hatalıysa geri bildirim döndürmeyi sağlar
                errors = Fonksiyonlar.control_PasswordData(username, email, name, surname, birthday, telephone,
                                                           password)
                if errors:
                    raise Exception(errors[0])

                # Girilen kullanıcı adı ve eposta daha önceden kayıtlı değilse kullanıcıyı ekler
                resultName: tuple = Database.searchKullanici_ByUsername(username)
                resultEmail: tuple = Database.searchKullanici_ByEmail(email)
                if resultName and resultEmail:
                    if (resultName[1] != resultEmail[1]) or (resultName[2] != resultEmail[2]):
                        raise Exception("Hesaba ait kullanıcı adı ve eposta uyuşmuyor.")
                    else:
                        if (resultName[6] != name or resultName[7] != surname or resultName[8] != birthday
                                or resultName[10] != telephone):
                            raise Exception("Hesaba ait girilen bilgiler uyuşmuyor.")
                        else:
                            user: Siniflar.Kullanici = Siniflar.Kullanici(
                                *resultName)  # Girdi olarak Tuple kullanıyoruz
                            user.set_sifre(password)
                            Database.updateKullanici(user)

                            session['username'] = username
                            return jsonify({'message': 'Şifre başarıyla değiştirildi.'}), 200

                # Kayıtlı olmayan bir eposta veya kullanıcı adı girildiyse hata döndürür
                else:
                    raise Exception("Bu kullanıcı adı veya epostaya sahip bir hesap yok.")

            elif action == "register":
                # Formdan gelen veriler
                username = request.form.get('username_register')
                password = request.form.get('password_register')
                email = request.form.get('email_register')
                location = request.form.get('location_register')
                interest = request.form.get('interest_register')  # İlgi alanları string olarak gelir
                name = request.form.get('name_register')
                surname = request.form.get('surname_register')
                birthday = request.form.get('birthday_register')
                gender = request.form.get('gender_register')
                telephone = request.form.get('telephone_register')

                # Profil fotoğrafını al
                profil_fotografi = request.files.get('profil_fotografi_register')
                fotograf_data = profil_fotografi.read() if profil_fotografi else None

                # Validasyonlar (örnek)
                if not username or not email or not name or not surname:
                    return {"error": "Gerekli alanlar doldurulmalıdır."}, 400

                if profil_fotografi and not profil_fotografi.content_type.startswith('image/'):
                    return {"error": "Geçersiz dosya formatı. Sadece .jpg kabul edilir."}, 400

                # Bilgilerin formatını kontrol edip hatalıysa geri bildirim döndürmeyi sağlar
                errors = Fonksiyonlar.control_RegisterData(username, password, email, location, interest, name,
                                                           surname, birthday, gender, telephone)
                if errors:
                    raise Exception(errors[0])

                # Girilen kullanıcı adı ve eposta daha önceden kayıtlı değilse kullanıcıyı ekler
                resultName = Database.searchKullanici_ByUsername(username)
                resultEmail = Database.searchKullanici_ByEmail(email)
                if not resultName and not resultEmail:

                    # Kullanıcı adı daha önceden kayıtlı değilse yeni kullanıcı oluşturma ve ekleme
                    new_User: Siniflar.Kullanici = (
                        Siniflar.Kullanici(ID=9999, kullanici_adi=username, sifre=password, email=email, konum=location,
                                           ilgi_alanlari=interest, ad=name, soyad=surname, dogum_tarihi=birthday,
                                           cinsiyet=gender, telefon_numarasi=telephone, profil_fotografi=fotograf_data))
                    Database.addKullanici(new_User)
                    session['username'] = username
                    return redirect(url_for('user_anasayfa'))

                # Girilen eposta veya kullanıcı adı önceden varsa uyarı mesajı döndürür
                # böylece hata alınmasını engeller
                else:
                    raise Exception("Bu kullanıcı adı veya eposta zaten mevcut.")

        # Hata alınması durumunda geri dönüş sağlanacak
        except Exception as error:
            print(f"Hata alındı: {error}")
            return jsonify({'error': str(error)}), 400

    return render_template('login.html')


# Anasayfa (user_anasayfa)
@app.route('/user_anasayfa')
def user_anasayfa():
    if 'username' not in session:
        return redirect(url_for('home'))
    username = session['username']
    kullanici_Bilgiler = Database.searchKullanici_ByUsername(session['username'])
    kullanici: Siniflar.Kullanici = Siniflar.Kullanici(*kullanici_Bilgiler)

    etkinlikler = []  # Kullanıcıya öneri olarak sunulacak etkinlik nesneleri
    gecici_etkinklikler = []
    siralanmis_etkinlikler = list()  # Etkinlikler öneri sistemine göre sıralanmış halinin tutacak liste
    # 1 - İLGİ ALANLARINA GÖRE BULMA
    # Kullanıcının ilgi alanlarına bağlı olarak etkinlik kategorileri bulur
    # İlgi alanlarının kategorilerine göre etkinlikleri bulup ekleyen kısım
    kullanici_ilgi_alanları = kullanici.get_ilgi_alanlari().split(",")
    ilgi_alanlarina_gore_kategori = list()
    if kullanici_ilgi_alanları:
        for ilgi_alani in kullanici_ilgi_alanları:
            bulunan_kategoriler = Database.searchKategori_ByIlgiAlan(ilgi_alani)
            if bulunan_kategoriler:
                bulunan_kategoriler = list(bulunan_kategoriler)
                for bulunan_kategori in bulunan_kategoriler:
                    ilgi_alanlarina_gore_kategori.append(bulunan_kategori[1])
    for kategori in ilgi_alanlarina_gore_kategori:
        bulunan_etkinlikler = Database.searchEtkinlik_ByCategory(kategori)
        if bulunan_etkinlikler:
            for etkinlik_bilgisi in bulunan_etkinlikler:
                etkinlik: Siniflar.Etkinlik = Siniflar.Etkinlik(*Database.searchEtkinlik_ByID(etkinlik_bilgisi[0]))
                if etkinlik not in etkinlikler:
                    etkinlikler.append(etkinlik)
    if etkinlikler:
        etkinlikler = Fonksiyonlar.etkinliklerGelecek(etkinlikler)
        siralanmis_etkinlikler = Fonksiyonlar.etkinlikSiralaUzaklik(kullanici.get_konum(), etkinlikler)

    # 2 - KATILDIĞI ETKİNLİĞİN İLGİ ALANINA GÖRE BULMA
    # Katıldığı etkinliklerin kategorisi ve ona bağlı olarak ilgi alanına göre
    # Etkinlikleri bulup ekler
    katildigi_etkinlikler = list()
    katildigi_etkinlikler_kategori = list()
    katildigi_etkinlikler_ilgi_alan = list()
    katilimci_bilgiler = Database.getAllKatilimci_ByKullaniciID(kullanici.get_ID())
    if katilimci_bilgiler:

        katilimci_bilgiler = list(katilimci_bilgiler)
        for katilimci_bilgi in katilimci_bilgiler:
            etkinlik_bilgisi = Database.searchEtkinlik_ByID(katilimci_bilgi[1])
            etkinlik: Siniflar.Etkinlik = Siniflar.Etkinlik(*etkinlik_bilgisi)
            katildigi_etkinlikler.append(etkinlik)

    olusturan_bilgiler = Database.getOlusturan_ByKullaniciID(kullanici.get_ID())
    if olusturan_bilgiler:
        for olusturan_bilgi in olusturan_bilgiler:
            etkinlik_bilgisi = Database.searchEtkinlik_ByID(olusturan_bilgi[0])
            etkinlik: Siniflar.Etkinlik = Siniflar.Etkinlik(*etkinlik_bilgisi)
            katildigi_etkinlikler.append(etkinlik)

    # Geçmişte katıldığı etkinlerin kategorisini bulur
    if katildigi_etkinlikler:
        for etkinlik in katildigi_etkinlikler:
            if not etkinlik.get_kategori() in katildigi_etkinlikler_kategori:
                katildigi_etkinlikler_kategori.append(etkinlik.get_kategori())

    # Katıldığı etkinliklerin kateogrisine bağlı olarak genel ilgi alanını bulur
    if katildigi_etkinlikler_kategori:
        for kategori in katildigi_etkinlikler_kategori:
            ilgi_alan = Database.searchKategori_ByCategory(kategori)[0][0]
            if not ilgi_alan in katildigi_etkinlikler_ilgi_alan:
                katildigi_etkinlikler_ilgi_alan.append(ilgi_alan)

    # Bulduğu ilgi alanlarına bağlı olarak, ilgi alanlarının bütün kategorilerini bulur
    bulunan_ilgi_alan_kategori = list()
    if katildigi_etkinlikler_ilgi_alan:
        for ilgi_alani in katildigi_etkinlikler_ilgi_alan:
            bulunan_kategoriler = Database.searchKategori_ByIlgiAlan(ilgi_alani)
            if bulunan_kategoriler:
                bulunan_kategoriler = list(bulunan_kategoriler)
                for bulunan_kategori in bulunan_kategoriler:
                    bulunan_ilgi_alan_kategori.append(bulunan_kategori[1])

    # Bulduğu kategorideki tüm etkinlikleri alır
    for kategori in bulunan_ilgi_alan_kategori:
        bulunan_etkinlikler = Database.searchEtkinlik_ByCategory(kategori)
        if bulunan_etkinlikler:
            for etkinlik_bilgisi in bulunan_etkinlikler:
                etkinlik: Siniflar.Etkinlik = Siniflar.Etkinlik(*Database.searchEtkinlik_ByID(etkinlik_bilgisi[0]))
                if etkinlik not in etkinlikler:
                    gecici_etkinklikler.append(etkinlik)

    if gecici_etkinklikler:
        gecici_etkinklikler = Fonksiyonlar.etkinliklerGelecek(gecici_etkinklikler)
        gecici_etkinlik_sirali = Fonksiyonlar.etkinlikSiralaUzaklik(kullanici.get_konum(), gecici_etkinklikler)
        for etkinlik in gecici_etkinlik_sirali:
            if etkinlik not in siralanmis_etkinlikler:
                siralanmis_etkinlikler.append(etkinlik)

    oneri_etkinlikler = list()
    oneri_etkinlik_idler = list()
    for etkinlik in siralanmis_etkinlikler:
        if etkinlik.get_ID() not in oneri_etkinlik_idler:
            oneri_etkinlikler.append(etkinlik)
            oneri_etkinlik_idler.append(etkinlik.get_ID())

    # Gelecekteki etkinlikleri belirleyip döndürür, çoktan tarihi geçmiş etkinlikler gelmez
    finalEvents = Fonksiyonlar.etkinliklerGelecek(oneri_etkinlikler)

    # Kullanıcının katıldığı veya oluşturduğu etkinlikleri getir
    already_events_info = Database.getAllKatilimci_ByKullaniciID(kullanici.get_ID())
    already_olusturan_events_info = Database.getOlusturan_ByKullaniciID(kullanici.get_ID())

    # Tüm etkinlikleri tek bir set içinde toplama
    already_events_id = set()

    # Kullanıcının katıldığı etkinliklerin ID'lerini ekle
    if already_events_info:
        already_events_id.update(event_bilgisi[1] for event_bilgisi in already_events_info)

    # Kullanıcının oluşturduğu etkinliklerin ID'lerini ekle
    if already_olusturan_events_info:
        already_events_id.update(event_bilgisi[0] for event_bilgisi in already_olusturan_events_info)

    # finalEvents listesinden zaten katıldığı/oluşturduğu etkinlikleri çıkar
    finalEvents = [event for event in finalEvents if event.get_ID() not in already_events_id]

    # Yeteri kadar etkinlik önerisi gelmezse en çok katılımcının olduğu etkinlikleri önerir
    most_user_events_info = Database.searchEtkinlik_ByParticipantCountFuture()
    most_user_events = []
    if most_user_events_info:
        for event_bilgi in most_user_events_info:
            newEtkinlik: Siniflar.Etkinlik = Siniflar.Etkinlik(*Database.searchEtkinlik_ByID(event_bilgi[0]))
            most_user_events.append(newEtkinlik)

    if finalEvents:
        uzunluk = abs(16 - len(finalEvents))
        if uzunluk > 16:
            uzunluk = 16
        most_user_events = most_user_events[0:uzunluk]
    else:
        most_user_events = most_user_events[:16]

    if most_user_events:
        for event in most_user_events:
            if event.get_ID() not in oneri_etkinlik_idler:
                finalEvents.append(event)
                oneri_etkinlik_idler.append(event.get_ID())

    if finalEvents:
        if len(finalEvents) > 16:
            finalEvents = finalEvents[:16]

    return render_template('user_anasayfa.html',
                           username=username,
                           kullanici=kullanici,
                           Database=Database,
                           events=finalEvents)


# Girilen etkinlik ismine göre etkinlikleri sıralayan kısım
@app.route('/search_events', methods=['GET', 'POST'])
def search_events():
    query = request.args.get('query', '').strip()  # Kullanıcıdan gelen sorgu
    etkinlikler = []

    if query:
        # Veritabanında etkinlik adını içerenleri ara
        etkinlik_bilgileri = Database.searchEtkinlik_ByName(query)
        if etkinlik_bilgileri:
            for etkinlik_bilgisi in etkinlik_bilgileri:
                # Etkinlik objesini oluştur ve listeye ekle
                newEtkinlik = Siniflar.Etkinlik(*etkinlik_bilgisi)
                etkinlikler.append(newEtkinlik)
    if etkinlikler:
        etkinlikler = etkinlikler[0:70]
    # Etkinliklerin sonuçlarını bir şablonda göster
    return render_template(
        'search_events.html',  # Arama sonuçlarını gösterecek HTML şablonu
        etkinlikler=etkinlikler,
        Database=Database
    )


# Etkinkliklerim kısmı
@app.route('/events')
def events():
    if 'username' not in session:
        return redirect(url_for('home'))
    username = session['username']
    kullanici_Bilgiler = Database.searchKullanici_ByUsername(session['username'])
    kullanici: Siniflar.Kullanici = Siniflar.Kullanici(*kullanici_Bilgiler)
    etkinlikler_Bilgiler = Database.getAllKatilimci_ByKullaniciID(kullanici.get_ID())
    etkinlikler_Bilgiler_olusturan = Database.getOlusturan_ByKullaniciID(kullanici.get_ID())
    if etkinlikler_Bilgiler:
        etkinlikler = [Siniflar.Etkinlik(*Database.searchEtkinlik_ByID(etkinlik_bilgisi[1]))
                       for etkinlik_bilgisi in etkinlikler_Bilgiler]
    else:
        etkinlikler = []

    if etkinlikler_Bilgiler_olusturan:
        for etkinlik_bilgisi in etkinlikler_Bilgiler_olusturan:
            print(etkinlik_bilgisi)
            etkinlikler.append(Siniflar.Etkinlik(*Database.searchEtkinlik_ByID(etkinlik_bilgisi[0])))

    return render_template('events.html',
                           username=username,
                           Database=Database,
                           kullanici=kullanici,
                           etkinlikler=etkinlikler)


@app.route('/filter_events', methods=['POST'])
def filter_events():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    username = session['username']
    kullanici_Bilgiler = Database.searchKullanici_ByUsername(username)
    kullanici = Siniflar.Kullanici(*kullanici_Bilgiler)
    etkinlikler_Bilgiler = Database.getAllKatilimci_ByKullaniciID(kullanici.get_ID())
    etkinlikler_Bilgiler_olusturan = Database.getOlusturan_ByKullaniciID(kullanici.get_ID())

    if etkinlikler_Bilgiler:
        etkinlikler = [Siniflar.Etkinlik(*Database.searchEtkinlik_ByID(etkinlik_bilgisi[1]))
                       for etkinlik_bilgisi in etkinlikler_Bilgiler]
    else:
        etkinlikler = []

    if etkinlikler_Bilgiler_olusturan:
        for etkinlik_bilgisi in etkinlikler_Bilgiler_olusturan:
            etkinlikler.append(Siniflar.Etkinlik(*Database.searchEtkinlik_ByID(etkinlik_bilgisi[0])))

    # AJAX ile gelen filtreleme ve sıralama parametrelerini al
    filter_type = request.json.get('filter_type', 'all')
    sort_type = request.json.get('sort_type', 'date')

    # Filtreleme
    if filter_type == 'my_events':
        etkinlikler = [etkinlik for etkinlik in etkinlikler if
                       Database.getOlusturan_ByEtkinlikID(etkinlik.get_ID())[0] == kullanici.get_ID()]
    elif filter_type == 'future_events':
        etkinlikler = [etkinlik for etkinlik in etkinlikler if
                       datetime.strptime(etkinlik.get_tarih(), '%Y-%m-%d') > datetime.now()]
    elif filter_type == 'past_events':
        etkinlikler = [etkinlik for etkinlik in etkinlikler if
                       datetime.strptime(etkinlik.get_tarih(), '%Y-%m-%d') < datetime.now()]

    # Sıralama
    if sort_type == 'date':
        etkinlikler.sort(key=lambda e: datetime.strptime(e.get_tarih(), '%Y-%m-%d'))
    elif sort_type == 'date-yakin':
        etkinlikler.sort(key=lambda e: datetime.strptime(e.get_tarih(), '%Y-%m-%d'), reverse=True)
    elif sort_type == 'duration':
        etkinlikler.sort(key=lambda e: e.get_etkinlik_suresi(), reverse=True)
    elif sort_type == 'duration-artan':
        etkinlikler.sort(key=lambda e: e.get_etkinlik_suresi())
    elif sort_type == 'participants':
        etkinlikler.sort(key=lambda e: len(Database.getAllKatilimci_ByEtkinlikID(e.get_ID()) or []) + 1, reverse=True)
    elif sort_type == 'participants-artan':
        etkinlikler.sort(key=lambda e: len(Database.getAllKatilimci_ByEtkinlikID(e.get_ID()) or []) + 1)

    # Etkinlikleri JSON formatında döndür
    etkinlikler_json = [
        {
            'id': etkinlik.get_ID(),
            'adi': etkinlik.get_etkinlik_adi(),
            'aciklama': etkinlik.get_aciklama(),
            'tarih': etkinlik.get_tarih().replace('-', '/'),
            'saat': etkinlik.get_saat(),
            'suresi': etkinlik.get_etkinlik_suresi(),
            'kategori': etkinlik.get_kategori(),
            'konum': etkinlik.get_konum(),
            'katilimci_sayisi': len(Database.getAllKatilimci_ByEtkinlikID(etkinlik.get_ID())) + 1,
            'etkinlik_photo': url_for('etkinlik_photo', etkinlik_id=etkinlik.get_ID()),
            'olusturan': {
                'isim': Database.searchKullanici_ByID(Database.getOlusturan_ByEtkinlikID(etkinlik.get_ID())[0])[6],
                'soyisim': Database.searchKullanici_ByID(Database.getOlusturan_ByEtkinlikID(etkinlik.get_ID())[0])[7],
                'username': Database.searchKullanici_ByID(Database.getOlusturan_ByEtkinlikID(etkinlik.get_ID())[0])[1]
            },
            'detay_linki': url_for('event_details', etkinlik_id=etkinlik.get_ID())
        }
        for etkinlik in etkinlikler
    ]

    return jsonify(etkinlikler_json)


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if 'username' not in session:
        return redirect(url_for('home'))
    username = session['username']
    kullanici_Bilgiler = Database.searchKullanici_ByUsername(username)
    kullanici: Siniflar.Kullanici = Siniflar.Kullanici(*kullanici_Bilgiler)
    kategoriler_bilgiler = Database.getAllKategoriler()
    if kategoriler_bilgiler:
        kategoriler = list(kategoriler_bilgiler)
        kategoriler = [kategori_bilgi[1] for kategori_bilgi in kategoriler]
    else:
        kategoriler = list()

    hazir_konumlar = Database.getAllKonumlar()
    if hazir_konumlar:
        hazir_konumlar = [konum[0] for konum in hazir_konumlar]
    else:
        hazir_konumlar = []
    if hazir_konumlar:
        hazir_konumlar = sorted(hazir_konumlar, key=locale.strxfrm)

    if request.method == 'POST':
        etkinlik_adi = request.form['etkinlikAdi']
        kategori = request.form['kategori']
        tarih = request.form['tarih']
        saat = request.form['saat']
        aciklama = request.form['aciklama']
        konum = request.form['konum']
        sure = request.form['sure']
        etkinlik_fotografi = request.files['etkinlikFotografi']

        # Fotoğrafı dönüştür ve kaydet
        fotograf_data = etkinlik_fotografi.read() if etkinlik_fotografi else None
        etkinlik_id = Database.getLastAddedEtkinlikID() + 1
        newEtkinlik: Siniflar.Etkinlik = Siniflar.Etkinlik(etkinlik_id, etkinlik_adi=etkinlik_adi, aciklama=aciklama,
                                                           tarih=tarih, saat=saat, etkinlik_suresi=sure, konum=konum,
                                                           kategori=kategori, etkinlik_fotografi=fotograf_data)
        Database.addEtkinlik(newEtkinlik)
        newOlusturan: Siniflar.Olusturan = Siniflar.Olusturan(kullanici.get_ID(), etkinlik_id)
        Database.addOlusturan(newOlusturan)
        print("Başarıyla oluşturuldu.")
        return redirect(url_for('events'))

    return render_template('create_event.html', username=username, kategoriler=kategoriler,
                           hazir_konumlar=hazir_konumlar)


@app.route('/update_event/<int:etkinlik_id>', methods=['GET', 'POST'])
def update_event(etkinlik_id):
    if 'username' not in session:
        return redirect(url_for('home'))

    username = session['username']
    kullanici_Bilgiler = Database.searchKullanici_ByUsername(username)
    kullanici: Siniflar.Kullanici = Siniflar.Kullanici(*kullanici_Bilgiler)

    # Etkinlik bilgilerini al
    etkinlik_bilgileri = Database.searchEtkinlik_ByID(etkinlik_id)
    if not etkinlik_bilgileri:
        return redirect(url_for('events'))  # Etkinlik bulunamazsa, etkinlikler sayfasına dön

    etkinlik_adi = etkinlik_bilgileri[1]
    etkinlik_aciklama = etkinlik_bilgileri[2]
    etkinlik_tarih = etkinlik_bilgileri[3]
    etkinlik_saat = etkinlik_bilgileri[4]
    etkinlik_sure = etkinlik_bilgileri[5]
    etkinlik_konum = etkinlik_bilgileri[6]
    etkinlik_kategori = etkinlik_bilgileri[7]

    kategoriler_bilgiler = Database.getAllKategoriler()
    kategoriler = [kategori[1] for kategori in kategoriler_bilgiler]

    hazir_konumlar = Database.getAllKonumlar()
    hazir_konumlar = [konum[0] for konum in hazir_konumlar]

    if request.method == 'POST':
        # Formdan gelen verilerle etkinlik güncelleme
        etkinlik_adi = request.form['etkinlikAdi']
        print(etkinlik_adi)
        kategori = request.form['kategori']
        tarih = request.form['tarih']
        saat = request.form['saat']
        aciklama = request.form['aciklama']
        konum = request.form['konum']
        sure = request.form['sure']
        etkinlik_fotografi = request.files['etkinlikFotografi']

        # Fotoğrafı dönüştür ve kaydet
        fotograf_data = etkinlik_fotografi.read() if etkinlik_fotografi else None

        updatedEtkinlik: Siniflar.Etkinlik = Siniflar.Etkinlik(
            ID=etkinlik_id, etkinlik_adi=etkinlik_adi, aciklama=aciklama,
            tarih=tarih, saat=saat, etkinlik_suresi=sure, konum=konum,
            kategori=kategori, etkinlik_fotografi=fotograf_data if fotograf_data else etkinlik_bilgileri[8]
        )

        Database.updateEtkinlik(updatedEtkinlik)
        return redirect(url_for('event_details', etkinlik_id=etkinlik_id))

    return render_template('update_event.html',
                           etkinlik_id=etkinlik_id,
                           etkinlik_adi=etkinlik_adi,
                           etkinlik_kategori=etkinlik_kategori,
                           etkinlik_tarih=etkinlik_tarih,
                           etkinlik_saat=etkinlik_saat,
                           etkinlik_aciklama=etkinlik_aciklama,
                           etkinlik_konum=etkinlik_konum,
                           etkinlik_sure=etkinlik_sure,
                           kategoriler=kategoriler,
                           hazir_konumlar=hazir_konumlar)


@app.route('/delete_event/<int:etkinlik_id>', methods=['POST'])
def delete_event(etkinlik_id):
    if 'username' not in session:
        return redirect(url_for('home'))

    username = session['username']
    kullanici_Bilgiler = Database.searchKullanici_ByUsername(username)
    kullanici: Siniflar.Kullanici = Siniflar.Kullanici(*kullanici_Bilgiler)

    # Etkinliği oluşturmuş olan kullanıcıyı al
    etkinlik_bilgileri = Database.searchEtkinlik_ByID(etkinlik_id)
    if etkinlik_bilgileri:

        # Etkinliği sil
        if Database.deleteEtkinlik(etkinlik_id):
            flash('Etkinlik başarıyla silindi!', 'success')
            return redirect(url_for('events'))  # Etkinlikler sayfasına yönlendir
        else:
            flash('Etkinlik silinirken bir hata oluştu.', 'danger')
            return redirect(url_for('events'))  # Hata durumunda yine etkinlikler sayfasına yönlendir
    else:
        flash('Etkinlik bulunamadı.', 'danger')
        return redirect(url_for('events'))


# Kullanıcının kendi profilini görmesini sağlayan fonksiyon
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('home'))

    username = session['username']
    kullanici_Bilgiler = Database.searchKullanici_ByUsername(username)
    kullanici: Siniflar.Kullanici = Siniflar.Kullanici(*kullanici_Bilgiler)
    etkinlikler_Bilgiler = Database.getAllKatilimci_ByKullaniciID(kullanici.get_ID())
    etkinlikler_Bilgiler_olusturan = Database.getOlusturan_ByKullaniciID(kullanici.get_ID())
    if etkinlikler_Bilgiler:
        etkinlikler = [Siniflar.Etkinlik(*Database.searchEtkinlik_ByID(etkinlik_bilgisi[1]))
                       for etkinlik_bilgisi in etkinlikler_Bilgiler]
    else:
        etkinlikler = []

    if etkinlikler_Bilgiler_olusturan:
        for etkinlik_bilgisi in etkinlikler_Bilgiler_olusturan:
            etkinlikler.append(Siniflar.Etkinlik(*Database.searchEtkinlik_ByID(etkinlik_bilgisi[0])))
    etkinlikler.sort(key=lambda e: datetime.strptime(e.get_tarih(), '%Y-%m-%d'), reverse=True)

    etkinlikler_dict = [
        {
            "ID": e.get_ID(),
            "etkinlik_adi": e.get_etkinlik_adi(),
            "aciklama": e.get_aciklama(),
            "tarih": e.get_tarih(),
            "saat": e.get_saat(),
            "etkinlik_suresi": e.get_etkinlik_suresi(),
            "konum": e.get_konum(),
            "kategori": e.get_kategori(),
        } for e in etkinlikler
    ]

    return render_template('profile.html',
                           username=username,
                           kullanici=kullanici,
                           kullanici_yas=Fonksiyonlar.hesaplaYas(kullanici.get_dogum_tarihi()),
                           kullanici_puan=Database.getTotalPuan(kullanici.get_ID()),
                           etkinlikler=etkinlikler,
                           etkinlikler_dict=etkinlikler_dict,
                           Database=Database
                           )


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Kullanıcıyı veritabanından çekme
    username = session['username']
    kullanici_Bilgiler = Database.searchKullanici_ByUsername(username)
    kullanici: Siniflar.Kullanici = Siniflar.Kullanici(*kullanici_Bilgiler)
    hazir_ilgi_alanlari = list(Database.getAllIlgiAlanlari())
    if hazir_ilgi_alanlari:
        hazir_ilgi_alanlari = [ilgi_alani[0] for ilgi_alani in hazir_ilgi_alanlari]
    else:
        hazir_ilgi_alanlari = []
    hazir_konumlar = Database.getAllKonumlar()
    if hazir_konumlar:
        hazir_konumlar = [konum[0] for konum in hazir_konumlar]
    else:
        hazir_konumlar = []
    if hazir_konumlar:
        hazir_konumlar = sorted(hazir_konumlar, key=locale.strxfrm)

    if request.method == 'POST':
        # Formdan gelen veriler
        kullanici_adi = request.form['kullanici_adi']
        email = request.form['email']
        konum = request.form['konum']
        ilgi_alanlari = ','.join(request.form.getlist('interests'))  # Seçilen ilgi alanlarını birleştir
        telefon_numarasi = request.form['telefon_numarasi']
        dogum_tarihi = request.form['dogum_tarihi']
        ad = request.form['ad']  # Yeni alan
        soyad = request.form['soyad']  # Yeni alan
        cinsiyet = request.form['cinsiyet']  # Yeni alan
        profil_fotografi = request.files['profil_fotografi'] if 'profil_fotografi' in request.files else None

        # Kullanıcı nesnesini güncelle
        kullanici.set_kullanici_adi(kullanici_adi)
        kullanici.set_email(email)
        kullanici.set_konum(konum)
        kullanici.set_ilgi_alanlari(ilgi_alanlari)
        kullanici.set_telefon_numarasi(telefon_numarasi)
        kullanici.set_dogum_tarihi(dogum_tarihi)
        kullanici.set_ad(ad)  # Yeni alanı güncelle
        kullanici.set_soyad(soyad)  # Yeni alanı güncelle
        kullanici.set_cinsiyet(cinsiyet)  # Yeni alanı güncelle

        if profil_fotografi:
            kullanici.set_profil_fotografi(profil_fotografi.read())

        # Veritabanını güncelle
        Database.updateKullanici(kullanici)

        return redirect(url_for('profile'))  # Güncellenen profile yönlendirme

    return render_template('edit_profile.html',
                           kullanici=kullanici,
                           Database=Database,
                           hazir_ilgi_alanlari=hazir_ilgi_alanlari,
                           hazir_konumlar=hazir_konumlar)


@app.route('/profile_photo/<int:user_id>')
def profile_photo(user_id):
    # Kullanıcının bilgilerini alın
    kullanici_Bilgiler = Database.searchKullanici_ByID(user_id)
    kullanici = Siniflar.Kullanici(*kullanici_Bilgiler)

    # Fotoğrafı alın
    photo_data = kullanici.get_profil_fotografi()  # BLOB formatındaki veri

    if photo_data:
        return send_file(
            io.BytesIO(photo_data),
            mimetype='image/jpeg',
            as_attachment=False
        )
    else:
        return "No photo found", 404


@app.route('/etkinlik_photo/<int:etkinlik_id>')
def etkinlik_photo(etkinlik_id):
    # Kullanıcının bilgilerini alın
    etkinlikBilgiler = Database.searchEtkinlik_ByID(etkinlik_id)
    etkinlik = Siniflar.Etkinlik(*etkinlikBilgiler)

    # Fotoğrafı alın
    photo_data = etkinlik.get_etkinlik_fotografi()  # BLOB formatındaki veri

    if photo_data:
        return send_file(
            io.BytesIO(photo_data),
            mimetype='image/jpeg',
            as_attachment=False
        )
    else:
        return "No photo found", 404


@app.route('/event_details/<int:etkinlik_id>')
def event_details(etkinlik_id):
    kullanici: Siniflar.Kullanici = Siniflar.Kullanici(*Database.searchKullanici_ByUsername(session['username']))
    etkinlikBilgiler = Database.searchEtkinlik_ByID(etkinlik_id)
    etkinlik: Siniflar.Etkinlik = Siniflar.Etkinlik(*etkinlikBilgiler)
    olusturan_id = Database.getOlusturan_ByEtkinlikID(etkinlik_id)[0]
    olusturan_kullanici: Siniflar.Kullanici = Siniflar.Kullanici(*Database.searchKullanici_ByID(olusturan_id))
    # Katilimci bilgileri
    katilimci_bilgiler = list(Database.getAllKatilimci_ByEtkinlikID(etkinlik_id))
    katilimcilar = list()
    if katilimci_bilgiler:
        for katilimci_bilgi in katilimci_bilgiler:
            katilimci: Siniflar.Kullanici = Siniflar.Kullanici(*Database.searchKullanici_ByID(katilimci_bilgi[0]))
            katilimcilar.append(katilimci)
    # Mesaj bilgileri
    etkinlik_mesajBilgiler = list(Database.getAllMesaj_ByEtkinlikID(etkinlik_id))
    etkinlik_mesajlar = list()
    if etkinlik_mesajBilgiler:
        for mesajBilgi in etkinlik_mesajBilgiler:
            mesaj = Siniflar.Mesaj(*mesajBilgi)
            etkinlik_mesajlar.append(mesaj)
    etkinlik_konum = etkinlik.get_konum()
    kullanici_konum = Siniflar.Kullanici(*Database.searchKullanici_ByUsername(session['username'])).get_konum()

    zaten_kayitli = 0
    katilinan_events = Database.getAllKatilimci_ByKullaniciID(kullanici.get_ID())
    olusturulan_events = Database.getOlusturan_ByKullaniciID(kullanici.get_ID())
    event_ids = []
    if katilinan_events:
        for event in katilinan_events:
            event_ids.append(event[1])
    if olusturulan_events:
        for event in olusturulan_events:
            event_ids.append(event[0])

    if etkinlik_id in event_ids:
        zaten_kayitli = 1

    return render_template('event_details.html',
                           username=session['username'],
                           kullanici=kullanici,
                           etkinlik=etkinlik,
                           etkinlik_konum=etkinlik_konum,
                           kullanici_konum=kullanici_konum,
                           olusturan_kullanici=olusturan_kullanici,
                           katilimcilar=katilimcilar,
                           etkinlik_mesajlar=etkinlik_mesajlar,
                           zaten_kayitli=zaten_kayitli,
                           Database=Database)


from datetime import datetime, timedelta


@app.route('/katilim_ekle', methods=['POST'])
def katilim_ekle():
    try:
        data = request.get_json()
        etkinlik_id = data.get('etkinlik_id')
        kullanici_id = data.get('kullanici_id')
        katilimci = Siniflar.Katilimci(kullanici_id, etkinlik_id)
        etkinlik = Siniflar.Etkinlik(*Database.searchEtkinlik_ByID(etkinlik_id))

        # Katılmak istenilen etkinliğin başlangıç ve bitiş zamanını hesapla
        etkinlik_baslangic = datetime.strptime(etkinlik.get_tarih() + " " + etkinlik.get_saat(), '%Y-%m-%d %H:%M')
        etkinlik_bitis = etkinlik_baslangic + timedelta(hours=etkinlik.get_etkinlik_suresi())

        # Kullanıcının katıldığı veya oluşturduğu diğer etkinlikleri al
        other_events = []
        other_events_info = Database.getAllKatilimci_ByKullaniciID(kullanici_id)
        other_events_info_creator = Database.getOlusturan_ByKullaniciID(kullanici_id)

        # Kullanıcının katıldığı etkinliklere dair bilgileri alır
        if other_events_info:
            for event_info in other_events_info:
                etkinlik: Siniflar.Etkinlik = Siniflar.Etkinlik(*Database.searchEtkinlik_ByID(event_info[1]))
                if etkinlik not in other_events:
                    other_events.append(etkinlik)

        # Kullanıcının oluşturduğu etkinliklere dair bilgileri alır
        if other_events_info_creator:
            for event_info in other_events_info_creator:
                etkinlik: Siniflar.Etkinlik = Siniflar.Etkinlik(*Database.searchEtkinlik_ByID(event_info[0]))
                if etkinlik not in other_events:
                    other_events.append(etkinlik)

        # Zaman çakışması kontrolü
        for other_event in other_events:
            other_event_baslangic = datetime.strptime(other_event.get_tarih() + " " + other_event.get_saat(),
                                                      '%Y-%m-%d %H:%M')
            other_event_bitis = other_event_baslangic + timedelta(hours=other_event.get_etkinlik_suresi())

            if (etkinlik_baslangic < other_event_bitis and etkinlik_bitis > other_event_baslangic):
                hataMesaj = (
                    f"\nBu etkinlik zamanında başka bir etkinliğiniz var:\n"
                    f"Etkinlik Adı: {other_event.get_etkinlik_adi()}\n"
                    f"Etkinlik Sahibi:"
                    f" {Database.searchKullanici_ByID(Database.getOlusturan_ByEtkinlikID(other_event.get_ID())[0])[6]}"
                    f" {Database.searchKullanici_ByID(Database.getOlusturan_ByEtkinlikID(other_event.get_ID())[0])[7]}"
                    f" @{Database.searchKullanici_ByID(Database.getOlusturan_ByEtkinlikID(other_event.get_ID())[0])[1]}\n"
                    f"Kategori: {other_event.get_kategori()}\n"
                    f"Başlangıç Saati: {other_event.get_tarih()} {other_event.get_saat()}\n"
                    f"Bitiş Saati: {other_event_bitis.strftime('%Y-%m-%d %H:%M')}")
                return jsonify({
                    "success": False,
                    "error": hataMesaj
                }), 400

        # Katılımı veritabanına ekle
        Database.addKatilimci(katilimci)

        # Başarılı işlem
        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/katilim_sil', methods=['POST'])
def katilim_sil():
    try:
        data = request.get_json()
        etkinlik_id = data.get('etkinlik_id')
        kullanici_id = data.get('kullanici_id')
        katilimci = Siniflar.Katilimci(kullanici_id, etkinlik_id)
        # Katılımı veritabanına ekle
        Database.deleteKatilimci(katilimci)

        # Başarılı işlem
        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/etkinlik_mesajlar/<int:etkinlik_id>')
def etkinlik_mesajlar(etkinlik_id):
    etkinlik_mesajBilgiler = list(Database.getAllMesaj_ByEtkinlikID(etkinlik_id))
    etkinlik_mesajlar = list()
    for mesajBilgi in etkinlik_mesajBilgiler:
        mesaj = Siniflar.Mesaj(*mesajBilgi)
        etkinlik_mesajlar.append(mesaj)

    # Mesajları HTML şablonuna gönder
    return render_template(
        'event_details.html',
        etkinlik_mesajlar=etkinlik_mesajlar,
        etkinlik_id=etkinlik_id,
    )


@app.route('/gonder_mesaj', methods=['POST'])
def gonder_mesaj():
    etkinlik_id = request.form.get('etkinlik_id')
    gonderen_ad = request.form.get('gonderen_ad')
    gonderen_kullanici_ad = gonderen_ad.split(" ")[-1].replace("@", "")
    gonderen_id = Database.searchKullanici_ByUsername(gonderen_kullanici_ad)[0]
    icerik = request.form.get('icerik')

    # # Mesajı veritabanına kaydet
    mesaj: Siniflar.Mesaj = Siniflar.Mesaj(99999, gonderici_id=gonderen_id, alici_id=etkinlik_id, mesaj_metni=icerik)
    Database.addMesaj(mesaj)

    # JSON formatında yanıt döndür
    return jsonify({'status': 'success', 'icerik': icerik, 'gonderen_ad': gonderen_ad})


# HENÜZ HİÇ KULLANILMADI AMA BELKİ İLERİDE KULLANILABİLİR
@app.route('/etkinlik_map/<int:etkinlik_id>')
def etkinlik_map(etkinlik_id):
    etkinlikBilgiler = Database.searchEtkinlik_ByID(etkinlik_id)
    etkinlik = Siniflar.Etkinlik(*etkinlikBilgiler)
    etkinlik_konum = etkinlik.get_konum()  # Assuming this returns a string like "Istanbul, Turkey"
    return render_template('etkinlik_map.html', etkinlik_konum=etkinlik_konum)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    session.pop('admin', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Database.checkAdmin(username, password):  # Admin bilgisi kontrol fonksiyonu
            session['admin'] = username  # Oturuma admin bilgisini kaydet
            return redirect(url_for('admin_page'))  # Başarılı giriş sonrası admin sayfasına yönlendir
        else:
            return render_template('admin_login.html', error="Kullanıcı adı veya şifre hatalı.")
    return render_template('admin_login.html')  # Giriş formunu göster


@app.route('/admin')
def admin_page():
    # Admin oturum kontrolü
    if 'admin' not in session:
        return redirect(url_for('admin_login'))  # Giriş yapmamışsa login sayfasına yönlendir

    pending_events_ids = Database.getAllPendingEvents()
    pending_Events = []
    for event_id in pending_events_ids:
        event = Database.searchEtkinlik_ByID(event_id[1])
        pending_Events.append(event)
    return render_template('admin.html', pending_events=pending_Events)


@app.route('/approve_event', methods=['POST'])
def approve_event():
    event_id = request.form.get('event_id')
    try:
        Database.approveEtkinlik(event_id)
        flash('Event approved successfully!', 'success')
    except Exception as e:
        flash(f'Error approving event: {e}', 'danger')
    return redirect(url_for('admin_page'))


@app.route('/admin_users')
def admin_users():
    # Admin oturum kontrolü
    if 'admin' not in session:
        return redirect(url_for('admin_login'))  # Giriş yapmamışsa login sayfasına yönlendir
    users = Database.getAllKullanicilar()  # Assuming this function returns a list of all users
    return render_template('admin_users.html', users=users)


@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    try:
        # Delete user relationships
        Database.deleteUserRelationships(user_id)
        # Delete user
        Database.deleteKullanici(user_id)
        flash('User deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting user: {e}', 'danger')
    return redirect(url_for('admin_users'))


@app.route('/admin_events')
def admin_events():
    # Admin oturum kontrolü
    if 'admin' not in session:
        return redirect(url_for('admin_login'))  # Giriş yapmamışsa login sayfasına yönlendir
    events = Database.getAllEtkinlikler()
    return render_template('admin_events.html', events=events)


@app.route('/delet_event', methods=['POST'])
def delet_event():
    event_id = request.form.get('event_id')
    try:

        Database.deleteEtkinlik(int(event_id))
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting event: {e}', 'danger')
    return redirect(url_for('admin_events'))


# Hesaptan çıkış yapmayı sağlayan fonksiyon
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/admin/logout', methods=['GET'])
def admin_logout():
    session.pop('admin', None)  # Admin oturumunu sonlandır
    return redirect(url_for('home'))  # Giriş sayfasına yönlendir


@app.route('/admin_event_details/<int:etkinlik_id>')
def admin_event_details(etkinlik_id):
    # Admin oturum kontrolü
    if 'admin' not in session:
        return redirect(url_for('admin_login'))  # Giriş yapmamışsa login sayfasına yönlendir
    etkinlikBilgiler = Database.searchEtkinlik_ByID(etkinlik_id)
    etkinlik: Siniflar.Etkinlik = Siniflar.Etkinlik(*etkinlikBilgiler)
    olusturan_id = Database.getOlusturan_ByEtkinlikID(etkinlik_id)[0]
    olusturan_kullanici: Siniflar.Kullanici = Siniflar.Kullanici(*Database.searchKullanici_ByID(olusturan_id))
    # Katilimci bilgileri
    katilimci_bilgiler = list(Database.getAllKatilimci_ByEtkinlikID(etkinlik_id))
    katilimcilar = list()
    if katilimci_bilgiler:
        for katilimci_bilgi in katilimci_bilgiler:
            katilimci: Siniflar.Kullanici = Siniflar.Kullanici(*Database.searchKullanici_ByID(katilimci_bilgi[0]))
            katilimcilar.append(katilimci)
    # Mesaj bilgileri
    etkinlik_mesajBilgiler = list(Database.getAllMesaj_ByEtkinlikID(etkinlik_id))
    etkinlik_mesajlar = list()
    if etkinlik_mesajBilgiler:
        for mesajBilgi in etkinlik_mesajBilgiler:
            mesaj = Siniflar.Mesaj(*mesajBilgi)
            etkinlik_mesajlar.append(mesaj)
    etkinlik_konum = etkinlik.get_konum()

    zaten_kayitli = 0

    event_ids = []

    if etkinlik_id in event_ids:
        zaten_kayitli = 1

    return render_template('admin_event_details.html',

                           etkinlik=etkinlik,
                           etkinlik_konum=etkinlik_konum,
                           olusturan_kullanici=olusturan_kullanici,
                           katilimcilar=katilimcilar,
                           etkinlik_mesajlar=etkinlik_mesajlar,
                           zaten_kayitli=zaten_kayitli,
                           Database=Database)


if __name__ == '__main__':
    app.run(debug=True)

