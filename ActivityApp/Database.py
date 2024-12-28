import sqlite3
from sqlite3 import connect

import Siniflar


# SQLite veritabanına bağlanma fonksiyonu
def connectDatabase(database_name="ActivityApp.db"):
    try:
        connection = sqlite3.connect(database_name)
        # print(f"{database_name} veritabanına başarıyla bağlanıldı.")
        return connection
    except sqlite3.Error as hata:
        print(f"Veritabanına bağlanırken hata oluştu: {hata}")
        return None


def getAllKullanicilar():
    connection = None
    try:
        connection = connectDatabase()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Kullanıcılar")
        kullanicilar = cursor.fetchall()
        return kullanicilar
    except sqlite3.Error as hata:
        print(f"Veritabanı hatası: {hata}")
        return []
    except Exception as hata:
        print(f"Beklenmeyen hata: {hata}")
        return []
    finally:
        if connection:
            connection.close()


def deleteUserRelationships(user_id):
    connection = connectDatabase()
    cursor = connection.cursor()
    try:
        # Delete user relationships (e.g., participation, creation, etc.)
        cursor.execute("DELETE FROM Katılımcılar WHERE kullanici_ID = ?", (user_id,))
        cursor.execute("DELETE FROM Olusturanlar WHERE kullanici_ID = ?", (user_id,))
        connection.commit()
    except sqlite3.Error as hata:
        print(f"Error deleting user relationships: {hata}")
    finally:
        connection.close()


def deleteKullanici(user_id):
    connection = connectDatabase()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Kullanıcılar WHERE ID = ?", (user_id,))
        connection.commit()
    except sqlite3.Error as hata:
        print(f"Error deleting user: {hata}")
    finally:
        connection.close()


def getAllEtkinlikler():
    connection = None
    try:
        connection = connectDatabase()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Etkinlikler")
        etkinlikler = cursor.fetchall()
        return etkinlikler
    except sqlite3.Error as hata:
        print(f"Veritabanı hatası: {hata}")
        return []
    except Exception as hata:
        print(f"Beklenmeyen hata: {hata}")
        return []
    finally:
        if connection:
            connection.close()


def deleteEventRelationships(event_id):
    connection = connectDatabase()
    cursor = connection.cursor()
    # Delete all participants related to the event
    query = "DELETE FROM Katılımcılar WHERE etkinlik_id = ?"
    cursor.execute(query, (event_id,))

    # Delete the creator of the event
    query = "DELETE FROM Olusturanlar WHERE etkinlik_id = ?"
    cursor.execute(query, (event_id,))

    # Delete all messages related to the event
    query = "DELETE FROM Mesajlar WHERE alici_id = ?"
    cursor.execute(query, (event_id,))

    # Commit the changes to the database
    connection.commit()


# Veritabanı tablolarını oluşturma fonksiyonu
def createTable():
    # Veritabanına bağlanma
    connection = connectDatabase()
    cursor = connection.cursor()

    # Tabloları oluşturmak için kullanılan SQL komutları
    kullanicilar_table = """
    CREATE TABLE IF NOT EXISTS Kullanıcılar (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        kullanici_adi TEXT UNIQUE NOT NULL,
        sifre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        konum TEXT,
        ilgi_alanlari TEXT,
        ad TEXT,
        soyad TEXT,
        dogum_tarihi DATE,
        cinsiyet TEXT,
        telefon_numarasi TEXT,
        profil_fotografi BLOB,
        FOREIGN KEY (konum) REFERENCES Konumlar(konum)
    );
    """

    etkinlikler_table = """
    CREATE TABLE IF NOT EXISTS Etkinlikler (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        etkinlik_adi TEXT NOT NULL,
        aciklama TEXT,
        tarih DATE NOT NULL,
        saat TIME,
        etkinlik_suresi INTEGER,
        konum TEXT,
        kategori TEXT,
        etkinlik_fotografi BLOB,
        FOREIGN KEY (konum) REFERENCES Konumlar(konum)
    );
    """

    etkinlikler_onay_table = """
    CREATE TABLE IF NOT EXISTS Etkinlikler_Onay (
        onay BOOLEAN NOT NULL,
        etkinlik_ID INTEGER PRIMARY KEY,
        FOREIGN KEY (etkinlik_ID) REFERENCES Etkinlikler(ID) ON DELETE CASCADE
    );
    """

    katilimcilar_table = """
    CREATE TABLE IF NOT EXISTS Katılımcılar (
        kullanici_ID INTEGER,
        etkinlik_ID INTEGER,
        FOREIGN KEY (kullanici_ID) REFERENCES Kullanıcılar(ID) ON DELETE CASCADE,
        FOREIGN KEY (etkinlik_ID) REFERENCES Etkinlikler(ID) ON DELETE CASCADE,
        PRIMARY KEY (kullanici_ID, etkinlik_ID)
    );
    """

    etkinlik_olusturanlar_table = """
    CREATE TABLE IF NOT EXISTS Olusturanlar (
        kullanici_ID INTEGER,
        etkinlik_ID INTEGER,
        FOREIGN KEY (kullanici_ID) REFERENCES Kullanıcılar(ID) ON DELETE CASCADE,
        FOREIGN KEY (etkinlik_ID) REFERENCES Etkinlikler(ID) ON DELETE CASCADE,
        PRIMARY KEY (kullanici_ID, etkinlik_ID)
    );
    """

    mesajlar_table = """
    CREATE TABLE IF NOT EXISTS Mesajlar (
        mesaj_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        gonderici_ID INTEGER NOT NULL,
        alici_ID INTEGER NOT NULL,
        mesaj_metni TEXT NOT NULL,
        gonderim_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (gonderici_ID) REFERENCES Kullanıcılar(ID) ON DELETE CASCADE,
        FOREIGN KEY (alici_ID) REFERENCES Etkinlikler(ID) ON DELETE CASCADE
    );
    """

    puanlar_table = """
    CREATE TABLE IF NOT EXISTS Puanlar (
        kullanici_ID INTEGER,
        etkinlik_ID INTEGER,
        puan INTEGER,
        kazanilan_tarih DATE,
        FOREIGN KEY (kullanici_ID) REFERENCES Kullanıcılar(ID) ON DELETE CASCADE,
        FOREIGN KEY (etkinlik_ID) REFERENCES Etkinlikler(ID) ON DELETE CASCADE,
        PRIMARY KEY (kullanici_ID, etkinlik_ID, kazanilan_tarih)
    );
    """

    konum_table = """
    CREATE TABLE IF NOT EXISTS Konumlar (
        konum TEXT PRIMARY KEY
    );
    """

    ilgi_alanlar_table = """
    CREATE TABLE IF NOT EXISTS İlgi_Alanlar (
        ilgi_alan TEXT PRIMARY KEY
    );
    """

    kategoriler_table = """
    CREATE TABLE IF NOT EXISTS Kategoriler (
        ilgi_alan TEXT,
        kategori TEXT,
        FOREIGN KEY (ilgi_alan) REFERENCES İlgi_Alanlar(ilgi_alan) ON DELETE CASCADE,
        PRIMARY KEY (ilgi_alan, kategori)
    );
    """

    admin_table = """
    CREATE TABLE IF NOT EXISTS Admin (
            username TEXT PRIMARY KEY,
            password TEXT
        );
    """

    # Tabloları oluşturma
    cursor.execute(kullanicilar_table)
    cursor.execute(etkinlikler_table)
    cursor.execute(etkinlikler_onay_table)
    cursor.execute(katilimcilar_table)
    cursor.execute(etkinlik_olusturanlar_table)
    cursor.execute(mesajlar_table)
    cursor.execute(puanlar_table)
    cursor.execute(konum_table)
    cursor.execute(ilgi_alanlar_table)
    cursor.execute(kategoriler_table)
    cursor.execute(admin_table)

    # Değişiklikleri kaydetme ve bağlantıyı kapatma
    connection.commit()
    connection.close()
    print("Tablolar başarıyla oluşturuldu.")


# KULLANICI FONKSİYONLARI
#  1- Kullanıcı ekleme fonksiyonu
def addKullanici(kullanici: Siniflar.Kullanici) -> None:
    try:
        connection = connectDatabase()
        cursor = connection.cursor()

        # Aynı kullanıcı adı olup olmadığını kontrol et
        cursor.execute("SELECT COUNT(*) FROM Kullanıcılar WHERE kullanici_adi = ?", (kullanici.get_kullanici_adi(),))
        if cursor.fetchone()[0] > 0:
            print("Bu kullanıcı adı zaten alınmış. Kullanıcı eklenmedi.")
            connection.close()
            return False

        # Aynı maile sahip kullanıcı olup olmadığını kontrol et
        cursor.execute("SELECT COUNT(*) FROM Kullanıcılar WHERE email = ?", (kullanici.get_email(),))
        if cursor.fetchone()[0] > 0:
            print("Bu kullanıcı maili zaten alınmış. Kullanıcı eklenmedi.")
            connection.close()
            return False

        # Kullanıcı eklerken kullanılacak SQl Komutu
        cursor.execute("""
                INSERT INTO Kullanıcılar (
                    kullanici_adi, sifre, email, konum, ilgi_alanlari, 
                    ad, soyad, dogum_tarihi, cinsiyet, telefon_numarasi, profil_fotografi
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
            kullanici.get_kullanici_adi(),
            kullanici.get_sifre(),
            kullanici.get_email(),
            kullanici.get_konum(),
            kullanici.get_ilgi_alanlari(),
            kullanici.get_ad(),
            kullanici.get_soyad(),
            kullanici.get_dogum_tarihi(),
            kullanici.get_cinsiyet(),
            kullanici.get_telefon_numarasi(),
            kullanici.get_profil_fotografi()
        ))
        connection.commit()
        connection.close()
        print("Kullanıcı başarıyla eklendi.")
        return True
    # Hataları yönetme
    except sqlite3.Error as hata:
        print(f"Kullanıcı eklenirken hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Kullanıcı eklenirken hata oluştu: {hata}")
        return False


# 2 - Kullanıcı bilgilerini güncelleme fonksiyonu
def updateKullanici(kullanici: Siniflar.Kullanici) -> None:
    try:
        # Veritabanına bağlanma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Güncelleme işlemi yaparken kullanılacak SQL komutu
        cursor.execute("""
                UPDATE Kullanıcılar
                SET kullanici_adi = ?, sifre = ?, email = ?, konum = ?, ilgi_alanlari = ?, 
                    ad = ?, soyad = ?, dogum_tarihi = ?, cinsiyet = ?, telefon_numarasi = ?, profil_fotografi = ?
                WHERE ID = ?
            """, (
            kullanici.get_kullanici_adi(),
            kullanici.get_sifre(),
            kullanici.get_email(),
            kullanici.get_konum(),
            kullanici.get_ilgi_alanlari(),
            kullanici.get_ad(),
            kullanici.get_soyad(),
            kullanici.get_dogum_tarihi(),
            kullanici.get_cinsiyet(),
            kullanici.get_telefon_numarasi(),
            kullanici.get_profil_fotografi(),
            kullanici.get_ID()
        ))
        # Değişiklikleri kaydetme ve bağlantıyı kapatma
        connection.commit()
        connection.close()
        print("Kullanıcı bilgileri başarıyla güncellendi.")
        return True
    # Hataları yönetme
    except sqlite3.Error as hata:
        print(f"Kullanıcı bilgileri güncellenirken hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Kullanıcı bilgileri güncellenirken hata oluştu: {hata}")
        return False


# 3 - Kullanıcı ID'si ile kullanıcı arama
def searchKullanici_ByID(kullanici_id: int):
    # Veritabanı ile bağlantı kurma
    connection = connectDatabase()
    cursor = connection.cursor()

    # Kullanıcı arama SQL Komutu
    cursor.execute("SELECT * FROM Kullanıcılar WHERE ID = ? ", (kullanici_id,))
    result = cursor.fetchone()

    # Sonuç döndürme
    connection.close()
    if result:
        return result
    else:
        print("Kullanıcı bulunamadı.")
        return None


# 4 - Kullanıcı e-posta adresi ile kullanıcı arama
def searchKullanici_ByEmail(eposta: str):
    # Veritabanı ile bağlantı kurma
    connection = connectDatabase()
    cursor = connection.cursor()

    # Kullanıcı arama SQL Komutu
    cursor.execute("SELECT * FROM Kullanıcılar WHERE email = ? ", (eposta,))
    result = cursor.fetchone()

    # Sonuç döndürme
    connection.close()
    if result:
        return result
    else:
        print("Kullanıcı bulunamadı.")
        return None


# 5 - Kullanıcı adı ile kullanıcı arama
def searchKullanici_ByUsername(kullanici_adi: str):
    # Veritabanı ile bağlantı kurma
    connection = connectDatabase()
    cursor = connection.cursor()

    # Kullanıcı arama SQL Komutu
    cursor.execute("SELECT * FROM Kullanıcılar WHERE kullanici_adi = ?", (kullanici_adi,))
    result = cursor.fetchone()

    # Sonuç döndürme
    connection.close()
    if result:
        return result
    else:
        print("Kullanıcı bulunamadı.")
        return None


# 6 - Kullanıcılar tablosundaki tüm ID'leri döndüren fonksiyon.
def getAllUserID():
    try:
        # Veritabanına bağlan
        connection = connectDatabase()
        cursor = connection.cursor()

        # Kullanıcılar tablosundaki tüm ID'leri al
        cursor.execute("SELECT ID FROM Kullanıcılar")
        ids = [row[0] for row in cursor.fetchall()]
        connection.close()
        return ids

    except Exception as error:
        print(f"Bir hata oluştu: {error}")
        return []


# 7 - Rastgele bir kullanıcı getiren fonksyion
def getRandomUser():
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Rastgele kullanıcı seçme sorgusu
        cursor.execute("""
            SELECT * 
            FROM Kullanıcılar
            ORDER BY RANDOM()
            LIMIT 1;
        """)

        # Kullanıcı bilgilerini al
        rastgele_kullanici = cursor.fetchone()
        connection.close()
        return rastgele_kullanici
    except sqlite3.Error as hata:
        print(f"Rastgele kullanıcı seçerken bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"Rastgele kullanıcı seçerken bir hata oluştu: {hata}")
        return None


# ETKİNLİK FONKSİYONLARI
# 1.1 - Etkinlik Ekleme Fonksiyonu
def addEtkinlik(etkinlik: Siniflar.Etkinlik):
    try:
        # Veritabanı ile bağlantı kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Etkinlik eklerken kullanılacak SQL Komutu
        cursor.execute("""
            INSERT INTO Etkinlikler (etkinlik_adi, aciklama, tarih, saat, etkinlik_suresi, konum, kategori, etkinlik_fotografi)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            etkinlik.get_etkinlik_adi(),
            etkinlik.get_aciklama(),
            etkinlik.get_tarih(),
            etkinlik.get_saat(),
            etkinlik.get_etkinlik_suresi(),
            etkinlik.get_konum(),
            etkinlik.get_kategori(),
            etkinlik.get_etkinlik_fotografi()
        ))
        connection.commit()
        connection.close()
        print("Etkinlik başarıyla eklendi.")
        # Etkinliği onay bekleme durumuna alır
        lastID = getLastAddedEtkinlikID()
        if lastID:
            etkinlikOnay: Siniflar.EtkinlikOnay = Siniflar.EtkinlikOnay(False, lastID)
            addEtkinlikOnay(etkinlikOnay)
            return True
        else:
            return False
    # Hataları yönetme
    except sqlite3.Error as hata:
        print(f"Etkinlik eklenirken bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Etkinlik eklenirken bir hata oluştu: {hata}")
        return False


# 1.2 - Etkinlik Silme Fonksiyonu
def deleteEtkinlik(etkinlik_id: int):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Etkinlikler_Onay WHERE etkinlik_ID = ?", (etkinlik_id,))
        cursor.execute("DELETE FROM Puanlar WHERE etkinlik_ID = ?", (etkinlik_id,))
        cursor.execute("DELETE FROM Olusturanlar WHERE etkinlik_ID = ?", (etkinlik_id,))
        cursor.execute("DELETE FROM Mesajlar WHERE alici_ID = ?", (etkinlik_id,))
        cursor.execute("DELETE FROM Katılımcılar WHERE etkinlik_ID = ?", (etkinlik_id,))

        # Etkinlikler tablosunda etkinliği silme
        cursor.execute("DELETE FROM Etkinlikler WHERE ID = ?", (etkinlik_id,))

        # Değişiklikleri kaydet
        connection.commit()
        connection.close()

        print(f"Etkinlik ID {etkinlik_id} başarıyla silindi.")
        return True
    # Hataları yönetme
    except sqlite3.Error as hata:
        print(f"Etkinlik silinirken bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Etkinlik silinirken bir hata oluştu: {hata}")
        return False


# 2 - Etkinlik Güncelleme Fonksiyonu
def updateEtkinlik(etkinlik: Siniflar.Etkinlik):
    try:
        # Veritabanı ile bağlantı kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Etkinlik güncellerken kullanılacak SQL Komutu
        cursor.execute("""
            UPDATE Etkinlikler
            SET etkinlik_adi = ?, aciklama = ?, tarih = ?, saat = ?, etkinlik_suresi = ?, konum = ?, kategori = ?, etkinlik_fotografi = ?
            WHERE ID = ?
        """, (
            etkinlik.get_etkinlik_adi(),
            etkinlik.get_aciklama(),
            etkinlik.get_tarih(),
            etkinlik.get_saat(),
            etkinlik.get_etkinlik_suresi(),
            etkinlik.get_konum(),
            etkinlik.get_kategori(),
            etkinlik.get_etkinlik_fotografi(),
            etkinlik.get_ID()
        ))
        connection.commit()
        connection.close()
        print("Etkinlik başarıyla güncellendi.")
        return True
    # Hataları yönetme
    except sqlite3.Error as hata:
        print(f"Etkinlik güncellenirken bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Etkinlik güncellenirken bir hata oluştu: {hata}")
        return False


# 3 - Etkinlik ID ile Etknilik Arama Fonksiyonu
def searchEtkinlik_ByID(etkinlik_ID: int):
    try:
        # Veritabanı ile bağlantı kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Etkinlik ID ile arama için SQL komutu
        cursor.execute("SELECT * FROM Etkinlikler WHERE ID = ?", (etkinlik_ID,))
        result = cursor.fetchone()
        connection.close()
        # Sonuç Döndürme
        if result:
            # print("Etkinlik bulundu:", result)
            return result
        else:
            print("Belirtilen ID'ye sahip bir etkinlik bulunamadı.")
            return None
    # Hata Kontrolü
    except sqlite3.Error as hata:
        print(f"Etkinlik aranırken bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"Etkinlik aranırken bir hata oluştu: {hata}")
        return None


# 4 - Kullanıcı Etkinlik Aratırken kullanılacak, Etkinlikleri isim ile aratma fonksiyonu
def searchEtkinlik_ByName(etkinlik_adi: str):
    try:
        # Veritabanı ile bağlantı kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Etkinlik arama için SQL komutu - aratılan adı içeren etkinlikleri bulur
        cursor.execute("SELECT * FROM Etkinlikler WHERE etkinlik_adi LIKE ?",
                       ('%' + etkinlik_adi + '%',))
        results = cursor.fetchall()
        connection.close()
        # Sonuç Döndürme
        if results:
            print("Eşleşen etkinlikler bulundu:")
            for row in results:
                print(row)
            return results
        else:
            print("Eşleşen bir etkinlik bulunamadı.")
            return None
    # Hata Kontrolü
    except sqlite3.Error as hata:
        print(f"Etkinlik aranırken bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"Etkinlik aranırken bir hata oluştu: {hata}")
        return None


# 5 - Kullanıcı Etkinlik Aratırken kullanılacak, Etkinlikleri Tarih ile aratma fonksiyonu
def searchEtkinlik_ByDate(tarih: str):
    try:
        # Veritabanı ile bağlantı kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Etkinlik arama için SQL komutu - aratılan tarihteki etkinlikleri bulur
        cursor.execute("SELECT * FROM Etkinlikler WHERE tarih = ?", (tarih,))
        results = cursor.fetchall()
        connection.close()
        # Sonuç Döndürme
        if results:
            print("Belirtilen tarihteki etkinlikler:")
            for row in results:
                print(row)
            return results
        else:
            print("Belirtilen tarihte etkinlik bulunamadı.")
            return None
    # Hata Kontrolü
    except sqlite3.Error as hata:
        print(f"Etkinlik aranırken bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"Etkinlik aranırken bir hata oluştu: {hata}")
        return None


# 6 - Kullanıcı Etkinlik Aratırken kullanılacak, Etkinlikleri Kategori ile aratma fonksiyonu
def searchEtkinlik_ByCategory(kategori: str):
    try:
        # Veritabanı ile bağlantı kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Etkinlik arama için SQL komutu - aratılan kategorideki etkinlikleri bulur
        cursor.execute("SELECT * FROM Etkinlikler WHERE kategori = ?", (kategori,))
        results = cursor.fetchall()
        connection.close()
        # Sonuç Döndürme
        if results:
            return results
        else:
            # print(f"{kategori} kategorisinde bir etkinlik bulunamadı.")
            return None
    # Hata Kontrolü
    except sqlite3.Error as hata:
        print(f"Etkinlik aranırken bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"Etkinlik aranırken bir hata oluştu: {hata}")
        return None


# Etkinlikleri katılımcı sayısına göre sıralayıp döndürür
def searchEtkinlik_ByParticipantCountFuture():
    try:
        # Veritabanı ile bağlantı kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Etkinlikleri katılımcı sayısına göre sıralama ve sadece gelecekteki etkinlikleri alma için SQL komutu
        cursor.execute("""
            SELECT E.*, COUNT(K.kullanici_ID) AS katilimci_sayisi
            FROM Etkinlikler E
            LEFT JOIN Katılımcılar K ON E.ID = K.etkinlik_ID
            WHERE E.tarih > CURRENT_DATE  -- Yalnızca gelecekteki etkinlikler
            GROUP BY E.ID
            ORDER BY katilimci_sayisi DESC
        """)

        results = cursor.fetchall()
        connection.close()

        # Sonuç döndürme
        if results:
            return results
        else:
            return None
    except sqlite3.Error as hata:
        print(f"Etkinlikler katılımcı sayısına göre sıralanırken bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"Etkinlikler katılımcı sayısına göre sıralanırken bir hata oluştu: {hata}")
        return None


# 8 - En son oluşturulan etkinliğin ID'sini döndüren fonksiyon
def getLastAddedEtkinlikID():
    connection = None
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # En son eklenen etkinliğin ID'sini al
        cursor.execute("SELECT ID FROM Etkinlikler ORDER BY ID DESC LIMIT 1")
        last_event_id = cursor.fetchone()

        connection.close()
        if last_event_id:
            return last_event_id[0]
        else:
            print("Etkinlikler tablosunda hiç etkinlik yok.")
            return None

    except sqlite3.Error as hata:
        print(f"Etkinlik ID aranırken bir hata oluştu: {hata}")
        connection.close()
        return None
    except Exception as hata:
        print(f"Etkinlik ID aranırken bir hata oluştu: {hata}")
        connection.close()
        return None


# ETKİNLİK ONAY FONKSİYONLARI
# 1 - Etkinlik Onay tablosuna veri ekleme fonksiyonu
def addEtkinlikOnay(etkinlikOnay: Siniflar.EtkinlikOnay):
    connection = None
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # EtkinlikOnay sınıfından verileri al
        onay = etkinlikOnay.get_onay()
        etkinlik_id = etkinlikOnay.get_etkinlik_id()

        # SQL sorgusu ile veriyi ekle
        cursor.execute("""
                INSERT INTO Etkinlikler_Onay (onay, etkinlik_ID)
                VALUES (?, ?)
            """, (onay, etkinlik_id))

        # Değişiklikleri kaydet
        connection.commit()
        connection.close()
        print(f"Etkinlik ID {etkinlik_id} için onay başarıyla eklendi.")

    except sqlite3.Error as hata:
        print(f"Etkinlik onayı eklenirken hata oluştu: {hata}")
        connection.close()
        return False
    except Exception as hata:
        print(f"Etkinlik onayı eklenirken hata oluştu: {hata}")
        connection.close()
        return False


# 2 - Etkinlik Onay tablosundaki veriyi güncelleme fonksiyonu
def updateEtkinlikOnay(etkinlikOnay: Siniflar.EtkinlikOnay):
    connection = None
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # EtkinlikOnay sınıfından verileri al
        onay = etkinlikOnay.get_onay()
        etkinlik_id = etkinlikOnay.get_etkinlik_id()

        # UPDATE işlemi yap
        cursor.execute("""
                        UPDATE Etkinlikler_Onay
                        SET onay = ?
                        WHERE etkinlik_ID = ?
                    """, (onay, etkinlik_id))
        print(f"Etkinlik ID {etkinlik_id} için onay başarıyla güncellendi.")

        # Değişiklikleri kaydet
        connection.commit()
        connection.close()

    except sqlite3.Error as hata:
        print(f"Etkinlik onayı eklenirken hata oluştu: {hata}")
        connection.close()
        return False
    except Exception as hata:
        print(f"Etkinlik onayı eklenirken hata oluştu: {hata}")
        connection.close()
        return False


# 3 - Etkinliğin onay durumunu döndürür
def getEtkinlikOnayDurumu(etkinlik_id: int):
    connection = None
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Etkinlik ID'sine göre onay durumunu sorgulayan SQL komutu
        cursor.execute("""
            SELECT onay
            FROM Etkinlikler_Onay
            WHERE etkinlik_ID = ?
        """, (etkinlik_id,))

        # Sonuçları al
        result = cursor.fetchone()
        connection.close()

        # Sonuç döndürme
        if result:
            return result[0]  # onay durumu döndürülür
        else:
            print(f"Etkinlik ID {etkinlik_id} için onay durumu bulunamadı.")
            return None

    except sqlite3.Error as hata:
        print(f"Etkinlik onay durumu sorgulanırken bir hata oluştu: {hata}")
        connection.close()
        return None
    except Exception as hata:
        print(f"Etkinlik onay durumu sorgulanırken bir hata oluştu: {hata}")
        connection.close()
        return None


# KATILIMCI FONKSİYONLARI
# 1 - Katılımcı Ekleme Fonksiyonu
def addKatilimci(katilimci: Siniflar.Katilimci):
    try:
        # Katılımcının etkinliğe daha önce katılıp katılmadığını kontrol et
        if getKatilimci(katilimci):
            # print(f"Kullanıcı ID {katilimci.get_kullanici_id()} zaten "
            #       f"Etkinlik ID {katilimci.get_etkinlik_id()} etkinliğine katılmış.")
            return False

        # Veritabanı bağlantısını kur
        connection = connectDatabase()
        cursor = connection.cursor()

        # Yeni katılmak istenen etkinlik bilgilerini al
        etkinlik_ID = katilimci.get_etkinlik_id()
        cursor.execute("SELECT tarih, saat, etkinlik_suresi FROM Etkinlikler WHERE ID = ?", (etkinlik_ID,))
        etkinlik = cursor.fetchone()

        if not etkinlik:
            print(f"Etkinlik ID {etkinlik_ID} bulunamadı.")
            connection.close()
            return False

        tarih, baslangic_saat, sure_saat = etkinlik
        baslangic_saat, baslangic_dakika = map(int, baslangic_saat.split(":"))
        bitis_saat = baslangic_saat + int(sure_saat)
        bitis_dakika = baslangic_dakika

        # Dakika taşmasını düzelt
        if bitis_dakika >= 60:
            bitis_saat += 1
            bitis_dakika -= 60

        # Aynı tarihte çakışan etkinlikleri kontrol et
        cursor.execute("""
            SELECT E.saat, E.etkinlik_suresi
            FROM Katılımcılar K
            INNER JOIN Etkinlikler E ON K.etkinlik_ID = E.ID
            WHERE K.kullanici_ID = ? AND E.tarih = ?
        """, (katilimci.get_kullanici_id(), tarih))

        katildigi_etkinlikler = cursor.fetchall()

        for katildigi in katildigi_etkinlikler:
            katilim_baslangic_saat, katilim_baslangic_dakika = map(int, katildigi[0].split(":"))
            katilim_sure_saat = katildigi[1]
            katilim_bitis_saat = katilim_baslangic_saat + int(katilim_sure_saat)
            katilim_bitis_dakika = katilim_baslangic_dakika

            # Dakika taşmasını düzelt
            if katilim_bitis_dakika >= 60:
                katilim_bitis_saat += 1
                katilim_bitis_dakika -= 60

            # Çakışma kontrolü
            if not (
                    (bitis_saat < katilim_baslangic_saat) or
                    (bitis_saat == katilim_baslangic_saat and bitis_dakika <= katilim_baslangic_dakika) or
                    (baslangic_saat > katilim_bitis_saat) or
                    (baslangic_saat == katilim_bitis_saat and baslangic_dakika >= katilim_bitis_dakika)
            ):
                print(f"Katılımcı ID {katilimci.get_kullanici_id()}, Etkinlik ID {etkinlik_ID} çakışıyor.")
                connection.close()
                return False

        # Katılımcı eklemek için SQL komutu
        cursor.execute("INSERT INTO Katılımcılar (kullanici_ID, etkinlik_ID) VALUES (?, ?)", (
            katilimci.get_kullanici_id(),
            etkinlik_ID
        ))
        connection.commit()
        connection.close()

        # Etkinliğe katıldığı için puan
        etkinlik_Tarih = tarih
        newPuan: Siniflar.Puan = Siniflar.Puan(katilimci.get_kullanici_id(), etkinlik_ID, 10, etkinlik_Tarih)
        addPuan(newPuan)

        # print("Katılımcı başarıyla eklendi.")
        return True
    except sqlite3.Error as hata:
        print(f"Katılımcı eklenirken bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Katılımcı eklenirken bir hata oluştu: {hata}")
        return False


# 2 - Katılımcı Silme Fonksiyonu
def deleteKatilimci(katilimci: Siniflar.Katilimci):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Katılımcıyı silmek için SQL komutu
        cursor.execute("DELETE FROM Katılımcılar WHERE kullanici_ID = ? AND etkinlik_ID = ?",
                       (katilimci.get_kullanici_id(), katilimci.get_etkinlik_id()))
        # Değişiklikleri kaydetme
        connection.commit()
        connection.close()

        # Etkinliğe katılmaktan vazgeçtiği için puan silme
        deletePuan(katilimci.get_kullanici_id(), katilimci.get_etkinlik_id())

        print("Katılımcı başarıyla silindi.")
        return True

    # Hata Kontrolü
    except sqlite3.Error as hata:
        print(f"Katılımcı silinirken bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Katılımcı silinirken bir hata oluştu: {hata}")
        return False


# 3 - Katılımcı arama fonksiyonu
def getKatilimci(katilimci: Siniflar.Katilimci):
    connection = None
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Kullanıcı ve etkinlik ID'sine göre katılımcının varlığını kontrol et
        cursor.execute("""
            SELECT * FROM Katılımcılar 
            WHERE kullanici_ID = ? AND etkinlik_ID = ?
        """, (katilimci.get_kullanici_id(), katilimci.get_etkinlik_id()))

        # Sonucu al
        katilimciBilgi = cursor.fetchone()
        connection.close()

        if katilimciBilgi:
            return katilimciBilgi  # Katılımcı zaten mevcut
        else:
            return False  # Katılımcı mevcut değil
    except sqlite3.Error as hata:
        print(f"Veritabanı hatası: {hata}")
        connection.close()
        return False
    except Exception as hata:
        print(f"Bir hata oluştu: {hata}")
        connection.close()
        return False


# 4 - Etkinlikteki bütün Katılımcıları arama fonksiyonu
def getAllKatilimci_ByEtkinlikID(etkinlik_id: int):
    connection = None
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # etkinlik ID'sine göre katılımcıların varlığını kontrol et
        cursor.execute("""
            SELECT * FROM Katılımcılar 
            WHERE etkinlik_ID = ?
        """, (etkinlik_id,))

        # Sonucu al
        katilimciBilgi = cursor.fetchall()
        connection.close()

        if katilimciBilgi:
            return katilimciBilgi
        else:
            return ""  # Katılımcılar mevcut değil

    except sqlite3.Error as hata:
        print(f"Veritabanı hatası: {hata}")
        connection.close()
        return False
    except Exception as hata:
        print(f"Bir hata oluştu: {hata}")
        connection.close()
        return False


# 5 - Kullanıcının katıldığı bütün etkinlikleri arama fonksiyonu
def getAllKatilimci_ByKullaniciID(kullanici_id: int):
    connection = None
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # kullanici ID'sine göre etkinliklerin bilgilerini tarih sırasına göre al
        cursor.execute("""
                    SELECT k.kullanici_ID, k.etkinlik_ID
                    FROM Katılımcılar k
                    INNER JOIN Etkinlikler e ON k.etkinlik_ID = e.ID
                    WHERE k.kullanici_ID = ?
                    ORDER BY e.tarih DESC, e.saat DESC
                """, (kullanici_id,))

        # Sonucu al
        katilimciBilgi = cursor.fetchall()
        connection.close()

        if katilimciBilgi:
            return katilimciBilgi
        else:
            return False  # Etkinlikler mevcut değil

    except sqlite3.Error as hata:
        print(f"Veritabanı hatası: {hata}")
        connection.close()
        return False
    except Exception as hata:
        print(f"Bir hata oluştu: {hata}")
        connection.close()
        return False


# OLUŞTURAN FONKSİYONLARI
# 1 - Oluşturan Ekleme Fonksiyonu
def addOlusturan(olusturan: Siniflar.Olusturan):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Oluşturan eklemek için SQL komutu
        cursor.execute("INSERT INTO Olusturanlar (kullanici_ID, etkinlik_ID) VALUES (?, ?)", (
            olusturan.get_kullanici_id(),
            olusturan.get_etkinlik_id()
        ))
        # Değişiklikleri kaydetme
        connection.commit()
        connection.close()

        # Etkinlik oluşturulduğu için puan
        etkinlik_Tarih = searchEtkinlik_ByID(olusturan.get_etkinlik_id())[3]
        newPuan: Siniflar.Puan = Siniflar.Puan(olusturan.get_kullanici_id(), olusturan.get_etkinlik_id(), 15,
                                               etkinlik_Tarih)
        addPuan(newPuan)
        print("Oluşturan başarıyla eklendi.")
        return True
    # Hata Kontrolü
    except sqlite3.Error as hata:
        print(f"Oluşturan eklenirken bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Oluşturan eklenirken bir hata oluştu: {hata}")
        return False


# 2 - Oluşturan Silme Fonksiyonu
def deleteOlusturan(olusturan: Siniflar.Olusturan):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Oluşturanı silmek için SQL komutu
        cursor.execute("DELETE FROM Olusturanlar WHERE kullanici_ID = ? AND etkinlik_ID = ?",
                       (olusturan.get_kullanici_id(), olusturan.get_etkinlik_id()))
        # Değişiklikleri kaydetme
        connection.commit()
        connection.close()

        # Etkinlik silinince oluşturulurken eklenen puan silinir,
        deletePuan(olusturan.get_kullanici_id(), olusturan.get_etkinlik_id())

        print("Oluşturan başarıyla silindi.")
        return True
    # Hata Kontrolü
    except sqlite3.Error as hata:
        print(f"Oluşturan silinirken bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Oluşturan silinirken bir hata oluştu: {hata}")
        return False


# 3 - Oluşturan kişinin ID'sini Etkinlik ID'ye göre arama
def getOlusturan_ByEtkinlikID(etkinlik_ID):
    connection = None
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Etkinlik ID'sine göre Oluşturan'ı sorgulama
        cursor.execute("""
            SELECT kullanici_ID FROM Olusturanlar WHERE etkinlik_ID = ?
        """, (etkinlik_ID,))

        # Sonuçları al
        olusturan = cursor.fetchone()
        connection.close()
        if olusturan:
            return olusturan  # Oluşturan kullanıcının bilgilerini döndürür
        else:
            print(f"Etkinlik ID {etkinlik_ID} için oluşturucu bulunamadı.")
            return None

    except sqlite3.Error as hata:
        print(f"Veritabanı hatası: {hata}")
        connection.close()
        return None
    except Exception as hata:
        print(f"Bir hata oluştu: {hata}")
        connection.close()
        return None


# 4 - Oluşturan kişinin ID'sini Etkinlik ID'ye göre arama
def getOlusturan_ByKullaniciID(kullanici_ID):
    connection = None
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # kullanici_ID'sine göre Oluşturan'ı sorgulama
        cursor.execute("""
            SELECT etkinlik_ID FROM Olusturanlar WHERE kullanici_ID = ?
        """, (kullanici_ID,))

        # Sonuçları al
        olusturan = cursor.fetchall()
        connection.close()
        if olusturan:
            return olusturan  # Kullanıcının oluşturudğu etkinlik bilgilerini döndürür
        else:
            print(f"{kullanici_ID} için etkinlik bulunamadı.")
            return None

    except sqlite3.Error as hata:
        print(f"Veritabanı hatası: {hata}")
        connection.close()
        return None
    except Exception as hata:
        print(f"Bir hata oluştu: {hata}")
        connection.close()
        return None


# MESAJ FONKSİYONLARI
# 1 - Mesaj Ekleme Fonksiyonu
def addMesaj(mesaj: Siniflar.Mesaj):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Mesaj eklemek için SQL komutu
        cursor.execute("INSERT INTO Mesajlar (gonderici_ID, alici_ID, mesaj_metni, gonderim_zamani)"
                       "VALUES (?, ?, ?, ?)", (
                           mesaj.get_gonderici_id(),
                           mesaj.get_alici_id(),
                           mesaj.get_mesaj_metni(),
                           mesaj.get_gonderim_zamani()
                       ))
        # Değişiklikleri kaydetme
        connection.commit()
        connection.close()
        print("Mesaj başarıyla eklendi.")
        return True
    # Hata Kontrolü
    except sqlite3.Error as hata:
        print(f"Mesaj eklenirken bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Mesaj eklenirken bir hata oluştu: {hata}")
        return False


# 2 - Etkinliğe ait tüm mesajları alma fonksiyonu
def getAllMesaj_ByEtkinlikID(etkinlik_ID: int):
    connection = None
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Mesaj eklemek için SQL komutu
        cursor.execute("SELECT * FROM Mesajlar WHERE alici_ID = ? ORDER BY gonderim_zamani ASC", (etkinlik_ID,))
        mesajlar = cursor.fetchall()
        # Değişiklikleri kaydetme
        connection.commit()
        connection.close()
        return mesajlar  # Mesajları döndürür
    # Hata Kontrolü
    except sqlite3.Error as hata:
        print(f"Mesaj eklenirken bir hata oluştu: {hata}")
        connection.close()
        return None
    except Exception as hata:
        print(f"Mesaj eklenirken bir hata oluştu: {hata}")
        connection.close()
        return None


# PUAN FONKSİYONLARI
# 1 - Puan Ekleme Fonksiyonu
def addPuan(puan: Siniflar.Puan):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Kullanıcının daha önce puanı olup olmadığını kontrol et
        cursor.execute("SELECT COUNT(*) FROM Puanlar WHERE kullanici_ID = ?", (puan.get_kullanici_id(),))
        puan_sayisi = cursor.fetchone()[0]

        # Bonus puan ekle
        bonus_puan = 20 if puan_sayisi == 0 else 0
        toplam_puan = puan.get_puan() + bonus_puan

        # Puan eklemek için SQL komutu
        cursor.execute(
            "INSERT INTO Puanlar (kullanici_ID, etkinlik_ID, puan, kazanilan_tarih) VALUES (?, ?, ?, ?)",
            (
                puan.get_kullanici_id(),
                puan.get_etkinlik_id(),
                toplam_puan,
                puan.get_kazanilan_tarih(),
            )
        )

        # Değişiklikleri kaydet
        connection.commit()
        connection.close()
        # print(f"Puan başarıyla eklendi. {('Bonus puan eklendi: +20' if bonus_puan else '')}")
        return True

        # Hata Kontrolü
    except sqlite3.Error as hata:
        print(f"Puan eklenirken bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Puan eklenirken bir hata oluştu: {hata}")
        return False


# 2 - Kullanıcıya ait toplam puanları döndürür
def getTotalPuan(kullanici_ID: int):
    connection = None
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Kullanıcının tüm puanlarını toplamak için SQL komutu
        cursor.execute("SELECT SUM(puan) FROM Puanlar WHERE kullanici_ID = ?", (kullanici_ID,))
        toplam_puan = cursor.fetchone()[0]

        # Bağlantıyı kapatma
        connection.close()

        # Eğer kullanıcıya ait puan yoksa toplamı 0 döndür
        return toplam_puan if toplam_puan else 0

    except sqlite3.Error as hata:
        print(f"Puan toplamı alınırken bir hata oluştu: {hata}")
        connection.close()
        return None
    except Exception as hata:
        print(f"Puan toplamı alınırken bir hata oluştu: {hata}")
        connection.close()
        return None


# 3 - Kullanıcının etkinlikten aldığı toplam puanı döndürür
def getEtkinlikPuan(kullanici_ID: int, etkinlik_ID: int, tarih):
    connection = None
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Kullanıcının tüm puanlarını toplamak için SQL komutu
        cursor.execute(
            "SELECT puan FROM Puanlar WHERE kullanici_ID = ? AND etkinlik_ID = ? AND kazanilan_tarih = ?",
            (kullanici_ID, etkinlik_ID, tarih)
        )

        puan = cursor.fetchone()

        # Bağlantıyı kapatma
        connection.close()

        # Eğer kullanıcıya ait puan yoksa toplamı 0 döndür
        return puan if puan else 0

    except sqlite3.Error as hata:
        print(f"Puan toplamı alınırken bir hata oluştu: {hata}")
        connection.close()
        return None
    except Exception as hata:
        print(f"Puan toplamı alınırken bir hata oluştu: {hata}")
        connection.close()
        return None


# 4 - Puan silme
def deletePuan(kullanici_id: int, etkinlik_id: int):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Kullanıcı ve etkinlik ID'sine göre puanı silmek için SQL komutu
        cursor.execute(
            "DELETE FROM Puanlar WHERE kullanici_ID = ? AND etkinlik_ID = ?",
            (kullanici_id, etkinlik_id)
        )

        # Değişiklikleri kaydet
        connection.commit()

        # Bağlantıyı kapat
        connection.close()

        print(f"Puan başarıyla silindi: Kullanıcı ID: {kullanici_id}, Etkinlik ID: {etkinlik_id}")
        return True

    # Hata Kontrolü
    except sqlite3.Error as hata:
        print(f"Puan silinirken bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Puan silinirken bir hata oluştu: {hata}")
        return False


# KONUM FONKSİYONLARI
# 1 - Konum ekleme fonksiyonu
def addKonum(konum: str):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Konumun daha önce eklenip eklenmediğini kontrol et
        cursor.execute("SELECT COUNT(*) FROM Konumlar WHERE konum = ?", (konum,))
        konum_sayisi = cursor.fetchone()[0]

        if konum_sayisi > 0:
            return False

        # Konumu eklemek için SQL komutu
        cursor.execute("INSERT INTO Konumlar (konum) VALUES (?)", (konum,))

        # Değişiklikleri kaydet
        connection.commit()
        connection.close()
        print(f"Konum '{konum}' başarıyla eklendi.")
        return True

    except sqlite3.Error as hata:
        print(f"Konum eklenirken bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Konum eklenirken bir hata oluştu: {hata}")
        return False


# 2 - Konum silme fonksiyonu
def deleteKonum(konum: str):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Konumun var olup olmadığını kontrol et
        cursor.execute("SELECT COUNT(*) FROM Konumlar WHERE konum = ?", (konum,))
        konum_sayisi = cursor.fetchone()[0]

        if konum_sayisi == 0:
            print(f"Konum '{konum}' bulunamadı.")
            return False

        # Konumu silme SQL komutu
        cursor.execute("DELETE FROM Konumlar WHERE konum = ?", (konum,))

        # Değişiklikleri kaydet
        connection.commit()
        connection.close()
        print(f"Konum '{konum}' başarıyla silindi.")
        return True

    except sqlite3.Error as hata:
        print(f"Konum silme sırasında bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Konum silme sırasında bir hata oluştu: {hata}")
        return False


# 3 - Konum arama fonksiyonu
def searchKonum(konum: str):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Konumu arama SQL komutu
        cursor.execute("SELECT * FROM Konumlar WHERE konum = ?", (konum,))
        result = cursor.fetchall()

        if result:
            print(f"Konum '{konum}' bulundu: {result}")
            return result
        else:
            print(f"Konum '{konum}' bulunamadı.")
            return None

    except sqlite3.Error as hata:
        print(f"Konum arama sırasında bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"Konum arama sırasında bir hata oluştu: {hata}")
        return None


# 4 - Konumları döndüren fonksiyon
def getAllKonumlar():
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Tüm konumları seçme SQL komutu
        cursor.execute("SELECT * FROM Konumlar")
        result = cursor.fetchall()

        if result:
            print("Tüm Konumlar:")
            for konum in result:
                print(konum)
            return result
        else:
            print("Hiç konum bulunamadı.")
            return None

    except sqlite3.Error as hata:
        print(f"Konumları getirirken bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"Konumları getirirken bir hata oluştu: {hata}")
        return None


# İLGİ ALANI FONKSİYONLARI
# 1 - İlgi Alanı ekleme fonksiyonu
def addIlgiAlani(ilgi_alani: str):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # İlgi alanının daha önce eklenip eklenmediğini kontrol et
        cursor.execute("SELECT COUNT(*) FROM İlgi_Alanlar WHERE ilgi_alan = ?", (ilgi_alani,))
        ilgi_alani_sayisi = cursor.fetchone()[0]

        if ilgi_alani_sayisi > 0:
            print(f"İlgi alanı '{ilgi_alani}' zaten mevcut.")
            return False

        # İlgi alanını eklemek için SQL komutu
        cursor.execute("INSERT INTO İlgi_Alanlar (ilgi_alan) VALUES (?)", (ilgi_alani,))

        # Değişiklikleri kaydet
        connection.commit()
        connection.close()
        print(f"İlgi alanı '{ilgi_alani}' başarıyla eklendi.")
        return True

    except sqlite3.Error as hata:
        print(f"İlgi alanı eklenirken bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"İlgi alanı eklenirken bir hata oluştu: {hata}")
        return False


# 2 - İlgi Alanı silme fonksiyonu
def deleteIlgiAlani(ilgi_alani: str):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # İlgi alanının var olup olmadığını kontrol et
        cursor.execute("SELECT COUNT(*) FROM İlgi_Alanlar WHERE ilgi_alan = ?", (ilgi_alani,))
        ilgi_alani_sayisi = cursor.fetchone()[0]

        if ilgi_alani_sayisi == 0:
            print(f"İlgi alanı '{ilgi_alani}' bulunamadı.")
            return False

        # İlgi alanını silme SQL komutu
        cursor.execute("DELETE FROM İlgi_Alanlar WHERE ilgi_alan = ?", (ilgi_alani,))

        # Değişiklikleri kaydet
        connection.commit()
        connection.close()
        print(f"İlgi alanı '{ilgi_alani}' başarıyla silindi.")
        return True

    except sqlite3.Error as hata:
        print(f"İlgi alanı silme sırasında bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"İlgi alanı silme sırasında bir hata oluştu: {hata}")
        return False


# 3 - İlgi Alanı arama fonksiyonu
def searchIlgiAlani(ilgi_alani: str):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # İlgi alanını arama SQL komutu
        cursor.execute("SELECT * FROM İlgi_Alanlar WHERE ilgi_alan = ?", (ilgi_alani,))
        result = cursor.fetchall()

        if result:
            print(f"İlgi alanı '{ilgi_alani}' bulundu: {result}")
            return result
        else:
            print(f"İlgi alanı '{ilgi_alani}' bulunamadı.")
            return None

    except sqlite3.Error as hata:
        print(f"İlgi alanı arama sırasında bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"İlgi alanı arama sırasında bir hata oluştu: {hata}")
        return None


# 4 - İlgi Alanlarını döndüren fonksiyon
def getAllIlgiAlanlari():
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Tüm ilgi alanlarını seçme SQL komutu
        cursor.execute("SELECT * FROM İlgi_Alanlar")
        result = cursor.fetchall()

        if result:
            # print("Tüm İlgi Alanları:")
            # for ilgi_alani in result:
            #     print(ilgi_alani)
            return result
        else:
            print("Hiç ilgi alanı bulunamadı.")
            return None

    except sqlite3.Error as hata:
        print(f"İlgi alanlarını getirirken bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"İlgi alanlarını getirirken bir hata oluştu: {hata}")
        return None


# KATEGORİ FONKSİYONLARI
# 1 - Kategori ekleme fonksiyonu
def addKategori(ilgi_alani: str, kategori: str):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # İlgi alanının var olup olmadığını kontrol et
        cursor.execute("SELECT COUNT(*) FROM İlgi_Alanlar WHERE ilgi_alan = ?", (ilgi_alani,))
        ilgi_alani_sayisi = cursor.fetchone()[0]

        if ilgi_alani_sayisi == 0:
            print(f"İlgi alanı '{ilgi_alani}' bulunamadı. Lütfen önce ekleyin.")
            return False

        # Kategorinin zaten mevcut olup olmadığını kontrol et
        cursor.execute("SELECT COUNT(*) FROM Kategoriler WHERE ilgi_alan = ? AND kategori = ?", (ilgi_alani, kategori))
        kategori_sayisi = cursor.fetchone()[0]

        if kategori_sayisi > 0:
            print(f"Kategori '{kategori}' zaten '{ilgi_alani}' ilgi alanına eklenmiş.")
            return False

        # Kategoriyi eklemek için SQL komutu
        cursor.execute("INSERT INTO Kategoriler (ilgi_alan, kategori) VALUES (?, ?)", (ilgi_alani, kategori))

        # Değişiklikleri kaydet
        connection.commit()
        connection.close()
        print(f"Kategori '{kategori}' başarıyla '{ilgi_alani}' ilgi alanına eklendi.")
        return True

    except sqlite3.Error as hata:
        print(f"Kategori eklenirken bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Kategori eklenirken bir hata oluştu: {hata}")
        return False


# 2 - Kategori silme fonksiyonu
def deleteKategori(ilgi_alani: str, kategori: str):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Kategorinin var olup olmadığını kontrol et
        cursor.execute("SELECT COUNT(*) FROM Kategoriler WHERE ilgi_alan = ? AND kategori = ?", (ilgi_alani, kategori))
        kategori_sayisi = cursor.fetchone()[0]

        if kategori_sayisi == 0:
            print(f"Kategori '{kategori}' '{ilgi_alani}' ilgi alanında bulunamadı.")
            return False

        # Kategoriyi silme SQL komutu
        cursor.execute("DELETE FROM Kategoriler WHERE ilgi_alan = ? AND kategori = ?", (ilgi_alani, kategori))

        # Değişiklikleri kaydet
        connection.commit()
        connection.close()
        print(f"Kategori '{kategori}' başarıyla '{ilgi_alani}' ilgi alanından silindi.")
        return True

    except sqlite3.Error as hata:
        print(f"Kategori silme sırasında bir hata oluştu: {hata}")
        return False
    except Exception as hata:
        print(f"Kategori silme sırasında bir hata oluştu: {hata}")
        return False


# 3 - Kategori arama fonksiyonu
def searchKategori(ilgi_alani: str, kategori: str):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Kategoriyi arama SQL komutu
        cursor.execute("SELECT * FROM Kategoriler WHERE ilgi_alan = ? AND kategori = ?", (ilgi_alani, kategori))
        result = cursor.fetchall()

        if result:
            return result
        else:
            # print(f"Kategori '{kategori}' '{ilgi_alani}' ilgi alanında bulunamadı.")
            return None

    except sqlite3.Error as hata:
        print(f"Kategori arama sırasında bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"Kategori arama sırasında bir hata oluştu: {hata}")
        return None


# 4 - Kategori arama fonksiyonu
def searchKategori_ByIlgiAlan(ilgi_alani: str):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Kategoriyi arama SQL komutu
        cursor.execute("SELECT * FROM Kategoriler WHERE ilgi_alan = ?", (ilgi_alani,))
        result = cursor.fetchall()

        if result:
            return result
        else:
            # print(f"'{ilgi_alani}' ilgi alanında bulunamadı.")
            return None

    except sqlite3.Error as hata:
        print(f"Kategori arama sırasında bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"Kategori arama sırasında bir hata oluştu: {hata}")
        return None


# 5 - Kategori arama fonksiyonu
def searchKategori_ByCategory(kategori: str):
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Kategoriyi arama SQL komutu
        cursor.execute("SELECT * FROM Kategoriler WHERE kategori = ?", (kategori,))
        result = cursor.fetchall()

        if result:
            return result
        else:
            # print(f"'{kategori}' kategori alanında bulunamadı.")
            return None

    except sqlite3.Error as hata:
        print(f"Kategori arama sırasında bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"Kategori arama sırasında bir hata oluştu: {hata}")
        return None


# 6 - Tüm Kategorileri döndüren fonksiyon
def getAllKategoriler():
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Tüm kategorileri seçme SQL komutu
        cursor.execute("SELECT * FROM Kategoriler")
        result = cursor.fetchall()

        if result:
            print("Tüm Kategoriler:")
            for kategori in result:
                print(kategori)
            return result
        else:
            print("Hiç kategori bulunamadı.")
            return None

    except sqlite3.Error as hata:
        print(f"Kategorileri getirirken bir hata oluştu: {hata}")
        return None
    except Exception as hata:
        print(f"Kategorileri getirirken bir hata oluştu: {hata}")
        return None


def getAllPendingEvents():
    """
    Retrieves all events that are pending approval from the database.
    """
    try:
        # Connect to the database
        conn = connectDatabase()
        cursor = conn.cursor()

        # SQL query to select all pending events
        query = """
        SELECT * FROM Etkinlikler_Onay WHERE onay= 0
        """
        cursor.execute(query)

        # Fetch all results
        pending_events = cursor.fetchall()

        # Close the connection
        conn.close()

        return pending_events

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []


def approveEtkinlik(etkinlik_id):
    """
    Approves the event with the given ID by updating its status in the database.

    :param etkinlik_id: ID of the event to be approved
    """
    try:
        # Connect to the database
        conn = connectDatabase()
        cursor = conn.cursor()

        # Update the event status to approved
        cursor.execute("""
            UPDATE Etkinlikler_Onay
            SET onay = 1
            WHERE etkinlik_ID = ?
        """, (etkinlik_id,))

        # Commit the changes
        conn.commit()

        # Check if the update was successful
        if cursor.rowcount == 0:
            print(f"No event found with ID {etkinlik_id}.")
        else:
            print(f"Event with ID {etkinlik_id} has been approved.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the database connection
        conn.close()



# Admin ekleme fonksiyonu
def addAdmin(username: str, password: str) -> bool:
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Adminin daha önce eklenip eklenmediğini kontrol et
        cursor.execute("SELECT COUNT(*) FROM Admin WHERE username = ?", (username,))
        admin_count = cursor.fetchone()[0]

        if admin_count > 0:
            print(f"Admin '{username}' zaten mevcut.")
            return False

        # Yeni admin eklemek için SQL komutu
        cursor.execute("INSERT INTO Admin (username, password) VALUES (?, ?)", (username, password))

        # Değişiklikleri kaydet
        connection.commit()
        connection.close()
        print(f"Admin '{username}' başarıyla eklendi.")
        return True

    except sqlite3.Error as error:
        print(f"Admin eklenirken bir hata oluştu: {error}")
        return False
    except Exception as error:
        print(f"Admin eklenirken bir hata oluştu: {error}")
        return False

# Admin bilgisi kontrol etme fonksiyonu
def checkAdmin(username: str, password: str) -> bool:
    try:
        # Veritabanı bağlantısını kurma
        connection = connectDatabase()
        cursor = connection.cursor()

        # Admin bilgilerini kontrol et
        cursor.execute("SELECT COUNT(*) FROM Admin WHERE username = ? AND password = ?", (username, password))
        admin_count = cursor.fetchone()[0]

        connection.close()
        if admin_count > 0:
            print("Admin bilgileri doğru.")
            return True
        else:
            print("Admin bilgileri hatalı.")
            return False

    except sqlite3.Error as error:
        print(f"Admin bilgisi kontrol edilirken bir hata oluştu: {error}")
        return False
    except Exception as error:
        print(f"Admin bilgisi kontrol edilirken bir hata oluştu: {error}")
        return False

# Fonksiyonu çağırarak tabloları oluşturma
#createTable()
# deleteEtkinlik(71)