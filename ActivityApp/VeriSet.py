import Siniflar
import Database
import Fonksiyonlar
import random
import string
from datetime import datetime, timedelta
import unicodedata
import re
import os

# Profil listeleri
erkek_profiller = []
kadin_profiller = []

# Erkek profil resimlerini alma
pp_klasor_erkek = "static/images/profilePhotos/erkek/"
for file_name in os.listdir(pp_klasor_erkek):
    if file_name.endswith(".jpg"):
        with open(os.path.join(pp_klasor_erkek, file_name), 'rb') as file:
            binary_photo_data = file.read()
            erkek_profiller.append(binary_photo_data)

# Kadın profil resimlerini alma
pp_klasor_kadin = "static/images/profilePhotos/kadin/"
for file_name in os.listdir(pp_klasor_kadin):
    if file_name.endswith(".jpg"):
        with open(os.path.join(pp_klasor_kadin, file_name), 'rb') as file:
            binary_photo_data = file.read()
            kadin_profiller.append(binary_photo_data)

turkiye_adlar = [
    "Ahmet", "Mehmet", "Ali", "Hasan", "Hüseyin", "Mustafa", "İbrahim", "Osman", "Yusuf", "Mahmut",
    "Fatih", "Kemal", "Burak", "Enes", "Serkan", "Emre", "Murat", "Çağlar", "Can", "Erkan",
    "Selim", "Hakan", "Ömer", "Volkan", "Erdem", "Oğuzhan", "Uğur", "Kaan", "Onur", "Yavuz",
    "Alper", "Furkan", "Göksel", "Harun", "Kadir", "Levent", "Mert", "Orhan", "Sinan", "Tamer",
    "Tayfun", "Utku", "Veli", "Zafer", "Arda", "Barış", "Cem", "Deniz", "Ege", "Ferhat",
    "Gökhan", "Halil", "İsmail", "Kerem", "Melih", "Nihat", "Oktay", "Rıza", "Sami", "Tuncay",
    "Vedat", "Yasin", "Zekeriya", "Ayla", "Leyla", "Sibel", "Elif", "Merve", "Zeynep", "Esra",
    "Aylin", "Bahar", "Ceren", "Ebru", "Neslihan", "Gizem", "Duygu", "Sevgi", "Aslı", "Feride",
    "Tuba", "Büşra", "Hacer", "Aysun", "Burcu", "Dilara", "Eda", "Filiz", "Gül", "Hülya",
    "İpek", "Jale", "Kadriye", "Lale", "Müjde", "Nazan", "Özlem", "Pelin", "Rana", "Seher",
    "Tülay", "Ümran", "Yelda", "Zehra", "Arzu", "Binnur", "Ceyda", "Dilek", "Emine", "Fadime",
    "Gülay", "Havva", "İlknur", "Jülide", "Kamile", "Leman", "Meral", "Nihal", "Özge", "Pervin",
    "Reyhan", "Selda", "Tülin", "Ülkü", "Yasemin", "Zübeyde", "Aydan", "Beyza", "Cansu", "Derya",
    "Esin", "Füsun", "Gülsüm", "Hatice", "İnci", "Kübra", "Lütfiye", "Medine", "Nergis", "Nur",
    "Oya", "Rabia", "Selin", "Şeyda", "Tuğba", "Üzeyir", "Yeşim", "Zinnur", "Doruk", "Çağlayan",
    "Çınar", "Çağlayan", "Pınar", "Bilge", "Tufan", "Sertan", "Buğra", "Oğuz", "Ercan"
]

erkek_isimleri = []
kadin_isimleri = []

# İsimleri ayırma
for isim in turkiye_adlar:
    if isim in [
        "Ahmet", "Mehmet", "Ali", "Hasan", "Hüseyin", "Mustafa", "İbrahim", "Osman", "Yusuf", "Mahmut",
        "Fatih", "Kemal", "Burak", "Enes", "Serkan", "Emre", "Murat", "Çağlar", "Can", "Erkan",
        "Selim", "Hakan", "Ömer", "Volkan", "Erdem", "Oğuzhan", "Uğur", "Kaan", "Onur", "Yavuz",
        "Alper", "Furkan", "Göksel", "Harun", "Kadir", "Levent", "Mert", "Orhan", "Sinan", "Tamer",
        "Tayfun", "Utku", "Veli", "Zafer", "Arda", "Barış", "Cem", "Deniz", "Ege", "Ferhat",
        "Gökhan", "Halil", "İsmail", "Kerem", "Melih", "Nihat", "Oktay", "Rıza", "Sami", "Tuncay",
        "Vedat", "Yasin", "Zekeriya", "Doruk", "Üzeyir", "Çağlayan", "Tufan", "Sertan", "Buğra", "Oğuz", "Ercan"
    ]:
        erkek_isimleri.append(isim)
    else:
        kadin_isimleri.append(isim)

turkiye_soyadlar = [
    "Yılmaz", "Kaya", "Demir", "Şahin", "Çelik", "Yıldız", "Arslan", "Doğan", "Kılıç", "Aslan",
    "Çetin", "Kara", "Koç", "Aydın", "Güneş", "Ak", "Kaplan", "Eroğlu", "Bozkurt", "Pek",
    "Şentürk", "Polat", "Bulut", "Bayram", "Uzun", "Taş", "Öztürk", "Turan", "Özdemir", "Çakır",
    "Aksoy", "Keskin", "Erdoğan", "Korkmaz", "Kurt", "Yavuz", "Uçar", "Güler", "Avcı", "Korkut",
    "Koçak", "Acar", "Sağlam", "Altun", "Soylu", "Ergin", "Kurtuluş", "Toprak", "Güneş", "Bayraktar",
    "Sezer", "Bilgin", "Çelik", "Doğanay", "İşler", "Kıran", "Şeker", "Ünal", "Şimşek", "Duman",
    "Akın", "Aydın", "Çoban", "Karaca", "Koca", "Demirtaş", "Boz", "Çevik", "Özkan", "Ertaş",
    "Kaplan", "Karakaş", "Işık", "Şen", "Orhan", "Çolak", "Başar", "Deniz", "Göksu", "Bilge",
    "Karahan", "Güzel", "Ekinci", "Tekin", "Özbek", "Görkem", "Atasoy", "Tan", "Kayaalp", "Yıldırım",
    "Önal", "Yurt", "Kalkan", "Balcı", "Çağlar", "Gökçe", "Özçelik", "Tosun", "Efe", "Çatal",
    "İnan", "Şentürk", "Aktaş", "Durmuş", "Kurtuluş", "Tanrıkulu", "Karataş", "Öztürk", "Demirbaş", "Şener",
    "Gürbüz", "Bozkurt", "Çakıroğlu", "Tekbaş", "Özdoğan", "Gökmen", "Sağ", "Akay", "Bayrak", "Taşkın",
    "Özdem", "Erden", "Karakoç", "Ekin", "Akşit", "Bulut", "Arıkan", "Soylu", "İşçi", "Sarı",
    "Durmaz", "Kaya", "Bilgili", "Dinç", "Aydemir", "Bayraktar", "Sönmez", "Çetinkaya", "Batur", "Uysal"
]

sehirler = [
        "İstanbul,Türkiye", "Ankara,Türkiye", "İzmir,Türkiye", "Bursa,Türkiye", "Antalya,Türkiye",
        "Adana,Türkiye", "Konya,Türkiye", "Gaziantep,Türkiye", "Kayseri,Türkiye", "Mersin,Türkiye",
        "Samsun,Türkiye", "Eskişehir,Türkiye", "Diyarbakır,Türkiye", "Denizli,Türkiye", "Balıkesir,Türkiye",
        "Malatya,Türkiye", "Sakarya,Türkiye", "Trabzon,Türkiye", "Erzurum,Türkiye", "Kocaeli,Türkiye",
        "Hatay,Türkiye", "Aydın,Türkiye", "Manisa,Türkiye", "Şanlıurfa,Türkiye", "Tekirdağ,Türkiye",
        "Çanakkale,Türkiye", "Van,Türkiye", "Ordu,Türkiye", "Afyonkarahisar,Türkiye", "Isparta,Türkiye"
    ]

# En çok sahip olunan 15 ilgi alanı
ilgi_alanlari = [
    "Müzik", "Spor", "Yemek Yapma", "Kitap Okuma", "Sinema",
    "Gezmek", "Teknoloji", "Fotoğrafçılık", "Resim Yapma", "Bahçecilik",
    "Yazılım Geliştirme", "Doğa Yürüyüşü", "Dans", "Yoga", "Oyun Oynamak",
    "Astronomi", "Makrome", "Kampçılık", "E-Spor", "Tasarım",
    "Tarih Araştırmaları"
]

ilgi_alani_resimleri = {}
# İlgi Alanına göre resimlerini alma
for ilgi_alan in ilgi_alanlari:
    ilgi_alani_resimleri[ilgi_alan] = list()
    etkinlik_pp_klasor = "static/images/ilgiAlani/" + ilgi_alan
    for file_name in os.listdir(etkinlik_pp_klasor):
        if file_name.endswith(".jpg"):
            with open(os.path.join(etkinlik_pp_klasor, file_name), 'rb') as file:
                binary_photo_data = file.read()
                ilgi_alani_resimleri[ilgi_alan].append(binary_photo_data)

# Popüler etkinlik kategorileri
kategoriler = {
    "Müzik": ["Canlı Müzik Gecesi", "Enstrüman Atölyesi", "Koro Çalışmaları"],
    "Spor": ["Amatör Spor Turnuvaları", "Fitness Workshopları", "Yüzme Etkinlikleri"],
    "Yemek Yapma": ["Gurme Yemek Atölyesi", "Dünya Mutfağı Deneyimleri", "Tatlı Yapma Kursu"],
    "Kitap Okuma": ["Kitap Kulübü Buluşmaları", "Yazar Söyleşileri", "Şiir Dinletileri"],
    "Sinema": ["Film Gösterimleri", "Kısa Film Çekim Workshopu", "Sinema Sohbetleri"],
    "Gezmek": ["Şehir Turları", "Doğa Keşif Gezileri", "Tarihi Mekan Ziyaretleri"],
    "Teknoloji": ["Yapay Zeka Seminerleri", "Yeni Teknolojiler Fuarı", "Kodlama Maratonu (Hackathon)"],
    "Fotoğrafçılık": ["Fotoğraf Sergileri", "Manzara Çekim Turları", "Drone Çekim Eğitimleri"],
    "Resim Yapma": ["Akrilik Boyama Atölyesi", "Sanat Sergileri", "Çizim Teknikleri Kursu"],
    "Bahçecilik": ["Bitki Bakım Atölyesi", "Bahçe Tasarımı Etkinlikleri", "Tohum Takas Günleri"],
    "Yazılım Geliştirme": ["Mobil Uygulama Hackathonu", "Oyun Geliştirme Eğitimleri", "Web Tasarım Çalıştayları"],
    "Doğa Yürüyüşü": ["Hiking ve Trekking Turları", "Kamp ve Doğa Hayatta Kalma Eğitimi", "Orman Keşif Gezileri"],
    "Dans": ["Tango ve Salsa Geceleri", "Hip-Hop Dans Workshopu", "Halk Dansları Eğitimi"],
    "Yoga": ["Açık Hava Yoga Seansları", "Meditasyon ve Esneklik Atölyesi", "Ruh ve Beden Dengesi Eğitimi"],
    "Oyun Oynamak": ["Board Game Geceleri", "E-Spor Turnuvaları", "Cosplay ve Oyun Festivalleri"],
    "Astronomi": ["Gökyüzü Gözlem Gecesi", "Uzay Bilimi Seminerleri", "Teleskop Kullanım Atölyesi"],
    "Makrome": ["Makrome Atölyeleri", "Dekoratif Düğüm Teknikleri Kursu", "Ev Tasarımı için Makrome"],
    "Kampçılık": ["Doğa ve Kampçılık Festival", "Kamp Malzemeleri Workshopu", "Hayatta Kalma Eğitimleri"],
    "E-Spor": ["LAN Parti Etkinlikleri", "Online Oyun Turnuvaları", "Profesyonel E-Spor Eğitimleri"],
    "Tasarım": ["Grafik Tasarım Çalıştayları", "3D Modelleme Eğitimleri", "Moda Tasarım Atölyeleri"],
    "Tarih Araştırmaları": ["Tarih Gezileri", "Tarihi Eser Sunumları", "Arkeolojik Kazı Turları"]
}

# Kategorilere özel etkinlik isimleri
# GEÇİCİ OLARAWK BU İSİMLER KULLANILIYOR DAHA SONRASINDA GÜNCELLENEBİLİR
# OPENAİ KÜTÜPHANESİ KULLANILARAK BELKİ
etkinlik_isimleri = {
    "Müzik": [
        "Ritim ve Melodi Gecesi", "Akustik Keyif", "Caz Gecesi", "Harmoni Festivali"
    ],
    "Spor": [
        "Yüksek Adrenalin Parkuru", "Açık Hava Yoga Seansı", "Futbol Çılgınlığı", "Sporun Kalbi: Maraton"
    ],
    "Yemek Yapma": [
        "Lezzet Avcıları", "Gurme Şef Atölyesi", "Tatlı Zamanı", "İtalyan Mutfağı Günü"
    ],
    "Kitap Okuma": [
        "Edebiyat Sohbetleri", "Kitap Kulübü Buluşması", "Roman Kahvesi", "Şiir Akşamı"
    ],
    "Sinema": [
        "Film Gecesi Maratonu", "Açık Hava Sineması", "Kült Filmler Akşamı", "Bağımsız Sinema Festivalı"
    ],
    "Gezmek": [
        "Doğa Keşif Turu", "Şehir Yolu", "Tarihi Yürüyüş", "Keşif Yolculuğu"
    ],
    "Teknoloji": [
        "Teknoloji Zirvesi", "Yapay Zeka Atölyesi", "Futuristik Hackathon", "Kodlama Dalgası"
    ],
    "Fotoğrafçılık": [
        "Doğanın İzinde Fotoğraf Turu", "Işık ve Gölge Çalıştayı", "Portre Çekim Atölyesi", "Gece Fotoğrafçılığı"
    ],
    "Resim Yapma": [
        "Sanatçı ile Canlı Resim", "Sulu Boya Çalıştayı", "Manzara Çizimi", "Yağlı Boya Atölyesi"
    ],
    "Bahçecilik": [
        "Bahçe Tasarımı", "Doğa ile Bütünleşme", "Sebze Yetiştirme Atölyesi", "Çiçeklerin Dünyası"
    ],
    "Yazılım Geliştirme": [
        "Yazılım Geliştirme Maratonu", "Açık Kaynak Konferansı", "Yazılım ve Yapay Zeka Atölyesi", "Web Tasarımı Workshop'u"
    ],
    "Doğa Yürüyüşü": [
        "Orman Yürüyüşü", "Göller Turu", "Dağcıların Buluşması", "Yaban Hayatı Keşfi"
    ],
    "Dans": [
        "Dans Gecesi", "Bale Atölyesi", "Modern Dans Festivali", "Salsa Çılgınlığı"
    ],
    "Yoga": [
        "Huzurlu Zihin: Yoga", "Doğada Yoga", "Gün Doğumu Seansı", "Zihin ve Beden Dengesi"
    ],
    "Oyun Oynamak": [
        "Video Oyunları Festivali", "Masa Oyunu Turnuvası", "Zeka Oyunları Maratonu", "E-Spor Yarışması"
    ],
    "Astronomi": [
        "Gökyüzü Gözlemi", "Yıldızlar Altında", "Astronomi Gecesi", "Evrenin Keşfi"
    ],
    "Makrome": [
        "Makrome Tasarım Atölyesi", "İpli Sanat Çalıştayı", "Makrome Takı Yapımı", "Doğal Doku Tasarımları"
    ],
    "Kampçılık": [
        "Orman Kampı", "Gece Kampı ve Ateş Sohbeti", "Doğa ile Yaşam", "Kampçılık Teknikleri Atölyesi"
    ],
    "E-Spor": [
        "E-Spor Turnuvası", "Oyun Şampiyonası", "Klanlar Arası Mücadele", "Online Şampiyonluk"
    ],
    "Tasarım": [
        "Grafik Tasarım Atölyesi", "Web Tasarım Workshop'u", "Yaratıcı Tasarım Zirvesi", "Tasarımcılar Buluşması"
    ],
    "Tarih Araştırmaları": [
        "Antik Uygarlıklar Konferansı", "Tarihi Yürüyüş", "Tarihi Keşif Turu", "Geçmişin İzinde"
    ]
}

etkinlik_aciklamalari = {
    "Müzik": {
        "Ritim ve Melodi Gecesi": [
            "Perküsyon enstrümanlarının eşlik ettiği bu gece, katılımcılara müzik ritimlerini keşfetme şansı sunuyor.",
            "Profesyonel müzisyenlerle ritim ve melodi üzerine interaktif bir performans gecesi.",
            "Hem dinleyip hem de eşlik edeceğiniz bir müzik deneyimi sizi bekliyor."
        ],
        "Akustik Keyif": [
            "Akustik tınıların büyüleyici etkisiyle keyifli bir akşam geçirebilirsiniz.",
            "Gitar ve vokalin mükemmel uyumuyla sakin bir müzik yolculuğuna hazır olun.",
            "Doğal ve sade melodilerin eşlik ettiği samimi bir atmosferde müzik keyfi."
        ],
        "Caz Gecesi": [
            "Cazın büyüleyici ritimlerine kapılacağınız unutulmaz bir akşam.",
            "Usta caz sanatçılarıyla dolu dolu bir müzik deneyimi sizi bekliyor.",
            "Caz müziğin efsane parçalarını dinleyerek harika bir gece geçirebilirsiniz."
        ],
        "Harmoni Festivali": [
            "Farklı müzik türlerinin bir araya geldiği çok renkli bir festival.",
            "Müzik dolu bu festivalde hem eğlenin hem yeni melodiler keşfedin.",
            "Sanatçılar ve grupların bir araya gelerek oluşturduğu eşsiz bir armoni deneyimi."
        ]
    },
    "Spor": {
        "Yüksek Adrenalin Parkuru": [
            "Heyecan verici zorlu etaplarda fiziksel sınırlarınızı zorlayın.",
            "Adrenalin dolu bir parkur macerasına hazır olun!",
            "Spor severlerin kalbini hızla attıracak zorlu bir macera sizi bekliyor."
        ],
        "Açık Hava Yoga Seansı": [
            "Doğanın içinde huzur bulacağınız bir yoga deneyimi.",
            "Açık havada bedeninizi ve zihninizi dinlendirecek bir etkinlik.",
            "Güne enerjik bir başlangıç yapmak için mükemmel bir fırsat."
        ],
        "Futbol Çılgınlığı": [
            "Futbol tutkunlarını bir araya getiren eğlenceli bir turnuva.",
            "Keyifli maçlarla dolu bir gün geçirebileceğiniz bir etkinlik.",
            "Amatör futbolseverler için hazırlanan bir futbol şöleni."
        ],
        "Sporun Kalbi: Maraton": [
            "Dayanıklılık ve azim gerektiren bu maratonda sınırlarınızı keşfedin.",
            "Spor tutkunları için düzenlenen bu maraton büyük bir buluşma noktası.",
            "Hem eğlenip hem spor yapacağınız bir etkinlikte yerinizi alın."
        ]
    },
    "Yemek Yapma": {
        "Lezzet Avcıları": [
            "Yemek yaparken lezzetleri yeniden keşfedeceğiniz bir atölye.",
            "Farklı mutfakların sırlarını öğreneceğiniz keyifli bir etkinlik.",
            "Tat ve tekniklerin buluştuğu, gurmeler için unutulmaz bir deneyim."
        ],
        "Gurme Şef Atölyesi": [
            "Profesyonel bir şefin rehberliğinde yemek yapmayı öğrenin.",
            "Gurme tariflerin sırlarını keşfetmek için mükemmel bir fırsat.",
            "Lezzet dolu tariflerle yemek yapmanın keyfini çıkarın."
        ],
        "Tatlı Zamanı": [
            "Farklı tatlı tariflerini deneyerek mutfağınızı şenlendirin.",
            "Tatlı yapmanın inceliklerini öğreneceğiniz bir etkinlik.",
            "Tatlı sevenler için tat dolu bir atölye."
        ],
        "İtalyan Mutfağı Günü": [
            "İtalyan mutfağının en sevilen yemeklerini yapmayı öğrenin.",
            "Lezzetli pizzalar ve makarnalarla dolu bir mutfak macerası.",
            "İtalyan mutfağını keşfetmek için lezzet dolu bir etkinlik."
        ]
    },
    "Kitap Okuma": {
        "Edebiyat Sohbetleri": [
            "Edebiyat severler için düzenlenen bu etkinlikte, farklı yazarların eserlerini tartışabilirsiniz.",
            "Kitaplar ve yazarlar üzerine derinlemesine sohbet edilecek bir etkinlik.",
            "Edebiyat dünyasında yeni keşifler yapabileceğiniz keyifli bir buluşma."
        ],
        "Kitap Kulübü Buluşması": [
            "Kitap tutkunlarının bir araya geldiği bu etkinlikte son okuduğunuz kitapları paylaşabilirsiniz.",
            "Her ay belirlenen bir kitabı okuyup üzerine tartışma fırsatı.",
            "Okuma deneyimlerinizi paylaşıp yeni kitap önerileri alabileceğiniz bir ortam."
        ],
        "Roman Kahvesi": [
            "Favori romanlarınızı kahve eşliğinde tartışacağınız bir etkinlik.",
            "Edebiyat ve kahve keyfini bir arada yaşayabileceğiniz bir buluşma.",
            "Roman kahramanları üzerine sohbetler eşliğinde samimi bir etkinlik."
        ],
        "Şiir Akşamı": [
            "Şairlerin eserlerinin okunduğu ve tartışıldığı bir akşam etkinliği.",
            "Kendi yazdığınız şiirleri paylaşabileceğiniz veya yeni şiirler keşfedebileceğiniz bir etkinlik.",
            "Şiirlerin büyülü dünyasında keyifli bir yolculuğa çıkın."
        ]
    },
    "Sinema": {
        "Film Gecesi Maratonu": [
            "Arka arkaya gösterilecek harika filmlerle dolu bir akşam.",
            "Klasiklerden modern eserlere kadar geniş bir film seçkisi.",
            "Film maratonuna katılarak sinema dolu bir gece geçirin."
        ],
        "Açık Hava Sineması": [
            "Yıldızlar altında en sevdiğiniz filmleri izleyebileceğiniz bir etkinlik.",
            "Açık havada, doğayla iç içe sinema keyfi sizi bekliyor.",
            "Doğa ve sinema tutkunlarını bir araya getiren büyüleyici bir deneyim."
        ],
        "Kült Filmler Akşamı": [
            "Sinema tarihine damga vuran kült filmlerin gösterimi.",
            "Filmleri izlerken sinema tutkunlarıyla fikir alışverişi yapabilirsiniz.",
            "Kült yapımların derinliklerine inmek için harika bir fırsat."
        ],
        "Bağımsız Sinema Festivalı": [
            "Bağımsız sinema eserlerini keşfedebileceğiniz bir festival.",
            "Farklı ülkelerden bağımsız yapımcıların eserleriyle dolu bir etkinlik.",
            "Sanatın sınırlarını zorlayan filmleri izleyebileceğiniz özel bir deneyim."
        ]
    },
    "Gezmek": {
        "Doğa Keşif Turu": [
            "Doğanın içinde huzur bulacağınız keyifli bir yürüyüş turu.",
            "Doğa tutkunları için hazırlanmış keşif dolu bir gezi.",
            "Bitki örtüsü ve yaban hayatını keşfetme fırsatı."
        ],
        "Şehir Yolu": [
            "Şehrin tarihi ve kültürel noktalarını keşfetmek için bir yürüyüş turu.",
            "Şehrin sokaklarında geçmişe yolculuk yapabileceğiniz bir etkinlik.",
            "Yerel hikayeler ve mimari detaylarla dolu bir gezi."
        ],
        "Tarihi Yürüyüş": [
            "Tarihi mekanlarda rehber eşliğinde keyifli bir yürüyüş.",
            "Geçmişin izlerini sürerek tarih dolu bir yolculuğa çıkın.",
            "Tarihi dokuyu yakından keşfetmek için eşsiz bir fırsat."
        ],
        "Keşif Yolculuğu": [
            "Yeni yerler keşfederek farklı kültürlerle tanışabileceğiniz bir etkinlik.",
            "Gezi tutkunları için özel olarak düzenlenmiş bir macera turu.",
            "Doğa, tarih ve keşif dolu bir gün sizi bekliyor."
        ]
    },
    "Teknoloji": {
        "Teknoloji Zirvesi": [
            "Teknolojinin geleceğini şekillendiren yeniliklerle dolu bir zirve.",
            "Lider teknoloji firmaları ve girişimcilerin buluşma noktası.",
            "Yenilikçi projeler ve fikirlerin sergilendiği bir etkinlik."
        ],
        "Yapay Zeka Atölyesi": [
            "Yapay zeka algoritmalarını öğrenebileceğiniz bir atölye.",
            "Geleceğin teknolojisi hakkında bilgi edinmek için harika bir fırsat.",
            "Uygulamalı yapay zeka projeleriyle dolu bir etkinlik."
        ],
        "Futuristik Hackathon": [
            "Yenilikçi fikirlerin hayat bulduğu bir yazılım geliştirme maratonu.",
            "Takım çalışmasıyla geleceğin teknolojilerini yaratma fırsatı.",
            "Kodlama ve teknoloji tutkunları için eşsiz bir deneyim."
        ],
        "Kodlama Dalgası": [
            "Kodlama öğrenmek isteyenler için interaktif bir atölye.",
            "Yeni başlayanlar ve uzmanlar için uygun seviyelerde etkinlikler.",
            "Kodlama dünyasına adım atmak için mükemmel bir fırsat."
        ]
    },
    "Fotoğrafçılık": {
        "Doğanın İzinde Fotoğraf Turu": [
            "Doğal güzellikleri fotoğraflamak için harika bir fırsat.",
            "Profesyonel rehberler eşliğinde doğa fotoğrafçılığı tekniklerini öğrenin.",
            "Doğanın büyüleyici manzaralarını keşfederek unutulmaz kareler yakalayın."
        ],
        "Işık ve Gölge Çalıştayı": [
            "Işık kullanımı ve gölge teknikleri üzerine uygulamalı bir atölye.",
            "Fotoğraflarınıza sanatsal bir dokunuş katmak için eşsiz bir deneyim.",
            "Fotoğrafçılıkta ışığın etkisini derinlemesine keşfedin."
        ],
        "Portre Çekim Atölyesi": [
            "Portre çekim tekniklerini uygulamalı olarak öğrenebileceğiniz bir etkinlik.",
            "Portre fotoğrafçılığında profesyonel ipuçlarını keşfedin.",
            "Modelle çalışarak yaratıcı portreler çekme deneyimi yaşayın."
        ],
        "Gece Fotoğrafçılığı": [
            "Gece manzaralarını yakalamak için gereken teknikleri öğrenin.",
            "Yıldızlar ve şehir ışıklarını fotoğraflayarak unutulmaz kareler yakalayın.",
            "Gece fotoğrafçılığında doğru ekipman ve ayarları keşfedin."
        ]
    },
    "Resim Yapma": {
        "Sanatçı ile Canlı Resim": [
            "Bir sanatçının rehberliğinde canlı bir resim deneyimi yaşayın.",
            "Sanatsal bir ortamda yeteneklerinizi geliştirmek için harika bir fırsat.",
            "Kendi tarzınızı keşfetmek için yaratıcı bir etkinlik."
        ],
        "Sulu Boya Çalıştayı": [
            "Sulu boya tekniklerini öğrenmek ve uygulamak için bir atölye.",
            "Renklerin ahengini kullanarak eşsiz eserler yaratın.",
            "Hem yeni başlayanlar hem de deneyimliler için uygun bir etkinlik."
        ],
        "Manzara Çizimi": [
            "Doğanın güzelliklerini kağıda dökmek için mükemmel bir fırsat.",
            "Manzara çizim teknikleri ve perspektif üzerine interaktif bir çalışma.",
            "Sanat dolu bir gün geçirmek isteyenler için keyifli bir etkinlik."
        ],
        "Yağlı Boya Atölyesi": [
            "Yağlı boya tekniklerini öğrenerek sanatsal eserler yaratın.",
            "Fırça darbeleriyle hayal gücünüzü tuvale taşıyın.",
            "Sanatçı rehberliğinde yağlı boya yapmanın keyfini çıkarın."
        ]
    },
    "Bahçecilik": {
        "Bahçe Tasarımı": [
            "Bahçenizi yeniden tasarlamak için yaratıcı fikirler ve uygulamalar.",
            "Bitkilerin yerleşimi ve düzeni üzerine pratik bilgiler edinin.",
            "Bahçe düzenlemesiyle doğayla uyum içinde bir alan yaratın."
        ],
        "Doğa ile Bütünleşme": [
            "Bitki yetiştirmenin huzur verici dünyasına adım atın.",
            "Bahçecilikte kullanılan doğal yöntemleri keşfedin.",
            "Doğayla iç içe bir etkinlikte kendinizi yenileyin."
        ],
        "Sebze Yetiştirme Atölyesi": [
            "Kendi sebzelerinizi yetiştirmeyi öğrenmek için bir rehber.",
            "Organik bahçecilik üzerine pratik bilgiler edinin.",
            "Doğal tarımla sağlıklı bir yaşam için ilk adımı atın."
        ],
        "Çiçeklerin Dünyası": [
            "Çiçek bakımı ve yetiştirme üzerine bilgi ve uygulamalar.",
            "Bahçenizi renklendirmek için çiçek seçimi ve düzenleme teknikleri.",
            "Çiçeklerin güzelliklerini keşfederek bahçecilik tutkunuzu geliştirin."
        ]
    },
    "Yazılım Geliştirme": {
        "Yazılım Geliştirme Maratonu": [
            "Yazılım projelerinizi geliştirmek için yoğun bir maraton.",
            "Takım çalışmasıyla yaratıcı projeler üretme fırsatı.",
            "Yazılım geliştirme dünyasında kendinizi sınayabileceğiniz bir etkinlik."
        ],
        "Açık Kaynak Konferansı": [
            "Açık kaynak yazılım dünyasına dair kapsamlı bilgi ve deneyim paylaşımı.",
            "Topluluklarla etkileşim kurarak projelerde yer alma şansı.",
            "Açık kaynak yazılım geliştirme hakkında farkındalık kazanabileceğiniz bir konferans."
        ],
        "Yazılım ve Yapay Zeka Atölyesi": [
            "Yapay zeka algoritmalarını yazılım projelerine entegre etmeyi öğrenin.",
            "Geleceğin teknolojileri üzerine uygulamalı bir çalışma.",
            "Yapay zeka ve yazılım dünyasının kesiştiği noktalarda yeni fikirler geliştirin."
        ],
        "Web Tasarımı Workshop'u": [
            "Web tasarımı için temel araç ve tekniklerin öğretildiği bir atölye.",
            "Kendi web sitenizi sıfırdan tasarlayabileceğiniz uygulamalı bir etkinlik.",
            "Modern web tasarım trendlerini öğrenip projelerinize uyarlayın."
        ]
    },
    "Doğa Yürüyüşü": {
        "Orman Yürüyüşü": [
            "Doğanın içinde huzurlu bir yürüyüşe çıkın.",
            "Ormanlık alanlarda temiz hava ve doğa keşfi dolu bir gün.",
            "Doğayla iç içe, stresten uzak bir yürüyüş etkinliği."
        ],
        "Göller Turu": [
            "Göller çevresinde yürüyüş yaparak muhteşem manzaralar keşfedin.",
            "Su kenarında huzurlu bir yürüyüşle doğayla bağlantı kurun.",
            "Göllerin büyüleyici güzelliğini fotoğraflama fırsatı."
        ],
        "Dağcıların Buluşması": [
            "Dağ yürüyüşü ve tırmanış tutkunları için bir araya gelme fırsatı.",
            "Rehber eşliğinde güvenli ve keyifli bir dağ yürüyüşü.",
            "Doğayla mücadele ederek sınırlarınızı zorlayın."
        ],
        "Yaban Hayatı Keşfi": [
            "Doğada yaban hayatını gözlemleyerek yeni türler keşfedin.",
            "Rehber eşliğinde doğanın saklı güzelliklerini keşfedeceğiniz bir yürüyüş.",
            "Doğa severler için eşsiz bir keşif fırsatı."
        ]
    },
    "Dans": {
        "Dans Gecesi": [
            "Renkli müzikler eşliğinde enerjik bir dans gecesi.",
            "Farklı dans stillerini deneyimleyerek eğlenceli vakit geçirin.",
            "Yeni arkadaşlarla tanışarak dans pistinin tadını çıkarın."
        ],
        "Bale Atölyesi": [
            "Profesyonel eğitmenler eşliğinde bale temel tekniklerini öğrenin.",
            "Esneklik ve zarafeti geliştiren bu etkinlik, her seviyeye uygundur.",
            "Sanat ve beden kontrolünü bir arada deneyimleyin."
        ],
        "Modern Dans Festivali": [
            "Çağdaş dans dünyasına adım atmak için eşsiz bir fırsat.",
            "Uluslararası ve yerel dans gruplarının gösterileriyle dolu bir gün.",
            "Yaratıcı koreografilerle dolu bu festivali kaçırmayın."
        ],
        "Salsa Çılgınlığı": [
            "Latin müzikleriyle coşkulu bir salsa gecesi.",
            "Partnerinizle veya yalnız katılabileceğiniz, eğlence dolu bir etkinlik.",
            "Dans figürlerinizi geliştirmek ve keyifli anılar biriktirmek için mükemmel bir fırsat."
        ]
    },
    "Yoga": {
        "Huzurlu Zihin: Yoga": [
            "Zihninizi ve bedeninizi dengelemek için meditasyon odaklı bir yoga seansı.",
            "Yoga pozlarını öğrenerek günlük stresinizi azaltın.",
            "Huzur dolu bir ortamda rahatlamayı deneyimleyin."
        ],
        "Doğada Yoga": [
            "Doğanın içinde, açık hava eşliğinde yoga pratiği.",
            "Kuş sesleri ve doğal güzellikler arasında eşsiz bir deneyim.",
            "Beden ve ruhunuzu doğanın enerjisiyle yenileyin."
        ],
        "Gün Doğumu Seansı": [
            "Güneşin ilk ışıklarıyla güne yoga ile başlayın.",
            "Enerjinizi yükseltmek için sabahın huzurlu anlarından faydalanın.",
            "Yeni başlayanlar ve deneyimliler için uygun bir etkinlik."
        ],
        "Zihin ve Beden Dengesi": [
            "Yoga ve meditasyonu birleştirerek iç huzurunuzu bulun.",
            "Profesyonel eğitmenlerle esneklik ve denge çalışmalarına katılın.",
            "Zihinsel ve fiziksel sağlığınızı güçlendirmek için harika bir fırsat."
        ]
    },
    "Oyun Oynamak": {
        "Video Oyunları Festivali": [
            "En yeni oyunları keşfetmek ve oynamak için harika bir etkinlik.",
            "Turnuvalara katılarak ödüller kazanma şansı.",
            "Hem retro hem de modern oyunlarla dolu eğlenceli bir ortam."
        ],
        "Masa Oyunu Turnuvası": [
            "Strateji ve zekanızı test edebileceğiniz rekabetçi bir turnuva.",
            "En sevilen masa oyunlarıyla dolu bir gün.",
            "Arkadaşlarınızla veya yeni tanıştığınız kişilerle keyifli vakit geçirin."
        ],
        "Zeka Oyunları Maratonu": [
            "Zekâ oyunlarında üstünlük sağlamak için yeteneklerinizi sergileyin.",
            "Mantık, hafıza ve yaratıcılıkla ilgili çeşitli oyunlar.",
            "Bireysel veya takım halinde yarışarak eğlenin."
        ],
        "E-Spor Yarışması": [
            "Popüler oyunlarda heyecan dolu e-spor müsabakaları.",
            "Profesyonel ve amatör oyuncular için rekabet dolu bir ortam.",
            "Oyun tutkunlarıyla bir araya gelip eğlenme şansı."
        ]
    },
    "Astronomi": {
        "Gökyüzü Gözlemi": [
            "Teleskoplarla yıldızları ve gezegenleri gözlemleme etkinliği.",
            "Uzman rehberler eşliğinde gökyüzünü keşfedin.",
            "Astronomi tutkunları için kaçırılmayacak bir deneyim."
        ],
        "Yıldızlar Altında": [
            "Gece boyunca yıldızlar ve takımyıldızları hakkında bilgi edinin.",
            "Doğanın sessizliğinde gökyüzünün büyüsünü yaşayın.",
            "Uzay meraklıları için eşsiz bir atmosfer."
        ],
        "Astronomi Gecesi": [
            "Astronomi seminerleri ve gökyüzü gözlemleriyle dolu bir gece.",
            "Evrendeki yerimizi anlamak için bilimsel bir yolculuk.",
            "Uzmanlarla birlikte yıldızlara bakarak öğrenme fırsatı."
        ],
        "Evrenin Keşfi": [
            "Evrenin sırlarını ve galaksilerin güzelliklerini keşfedin.",
            "Bilim insanlarıyla astronomi üzerine keyifli sohbetler.",
            "Uzayı ve gezegenleri anlamak için heyecan verici bir etkinlik."
        ]
    },
    "Makrome": {
        "Makrome Tasarım Atölyesi": [
            "Kendi makrome tasarımlarınızı yapmayı öğrenin.",
            "El becerilerinizi geliştirmek için uygulamalı bir atölye.",
            "Dekoratif objeler tasarlayarak keyifli zaman geçirin."
        ],
        "İpli Sanat Çalıştayı": [
            "Farklı ip teknikleriyle yaratıcı sanat eserleri oluşturun.",
            "Makrome ve düğüm sanatının temel tekniklerini öğrenin.",
            "Sanatseverlerle bir araya gelerek güzel bir gün geçirin."
        ],
        "Makrome Takı Yapımı": [
            "El yapımı bileklik ve kolye tasarlamayı öğrenin.",
            "Şık ve yaratıcı takılar yaparak becerilerinizi geliştirin.",
            "Makrome takı sanatında kendinizi ifade etmenin yollarını keşfedin."
        ],
        "Doğal Doku Tasarımları": [
            "Doğal malzemelerle şık makrome tasarımlar yapın.",
            "Ev dekorasyonunuza uygun objeler tasarlayın.",
            "Makrome sanatının sınırlarını zorlamak için yaratıcı bir etkinlik."
        ]
    },
    "Kampçılık": {
        "Orman Kampı": [
            "Doğanın içinde kamp yaparak huzurlu bir hafta sonu geçirin.",
            "Ormanda güvenli kamp kurma tekniklerini öğrenin.",
            "Arkadaşlarınızla veya ailenizle unutulmaz bir deneyim yaşayın."
        ],
        "Gece Kampı ve Ateş Sohbeti": [
            "Yıldızların altında ateş başında keyifli sohbetler.",
            "Gece boyunca kamp alanında dinlendirici bir atmosfer.",
            "Doğayla baş başa kalmanın tadını çıkarın."
        ],
        "Doğa ile Yaşam": [
            "Kamp yaparken doğanın enerjisini hissedin.",
            "Hayatta kalma becerileri üzerine uygulamalı bir eğitim.",
            "Kendinizi doğanın bir parçası olarak yeniden keşfedin."
        ],
        "Kampçılık Teknikleri Atölyesi": [
            "Kamp yaparken ihtiyacınız olan temel teknikleri öğrenin.",
            "Çadır kurma, ateş yakma ve doğada yön bulma gibi bilgiler edinin.",
            "Doğada rahat bir kamp deneyimi için eşsiz bir etkinlik."
        ]
    },
    "E-Spor": {
        "E-Spor Turnuvası": [
            "Popüler oyunlarda rekabet dolu bir turnuva.",
            "En iyi oyuncularla bir araya gelerek yeteneklerinizi sergileyin.",
            "Oyun dünyasında tanınma fırsatı ve ödüller kazanma şansı."
        ],
        "Oyun Şampiyonası": [
            "Büyük ödüller için çekişmeli e-spor müsabakaları.",
            "Hem bireysel hem de takım olarak katılabileceğiniz bir etkinlik.",
            "Oyun dünyasının en iyi oyuncularıyla tanışma fırsatı."
        ],
        "Klanlar Arası Mücadele": [
            "Ekip ruhunu ve strateji becerilerinizi geliştirin.",
            "Takım arkadaşlarınızla birlikte zafer için mücadele edin.",
            "Rekabetçi bir ortamda oyun keyfini doruklarda yaşayın."
        ],
        "Online Şampiyonluk": [
            "Çevrimiçi platformda organize edilen büyük bir e-spor etkinliği.",
            "Dünyanın dört bir yanından oyuncularla mücadele edin.",
            "Heyecan verici oyunlar ve büyük ödüller sizi bekliyor."
        ]
    },
    "Tasarım": {
        "Grafik Tasarım Atölyesi": [
            "Profesyonel tasarım araçlarını öğrenerek yaratıcı projeler oluşturun.",
            "Grafik tasarım dünyasına giriş yapmak isteyenler için ideal bir etkinlik.",
            "Deneyimli eğitmenlerle interaktif bir tasarım atölyesi."
        ],
        "Web Tasarım Workshop'u": [
            "Modern web tasarım trendleri ve araçları üzerine uygulamalı bir çalışma.",
            "Kendi web sitenizi sıfırdan tasarlamayı öğrenin.",
            "Hem teknik bilgi hem de estetik bakış açısı kazanın."
        ],
        "Yaratıcı Tasarım Zirvesi": [
            "Tasarım dünyasının profesyonelleriyle bir araya gelin.",
            "Farklı tasarım disiplinleri üzerine ilham verici konuşmalar.",
            "Tasarım projelerinizde yeni bakış açıları geliştirin."
        ],
        "Tasarımcılar Buluşması": [
            "Tasarım tutkunları ve profesyonellerle bir araya gelme fırsatı.",
            "Yeni bağlantılar kurarak fikirlerinizi paylaşın.",
            "Tasarım dünyasında yaratıcı bir ortamda bulunma şansı."
        ]
    },
    "Tarih Araştırmaları": {
        "Antik Uygarlıklar Konferansı": [
            "Geçmiş uygarlıkların kültürleri ve yapıları hakkında derinlemesine bilgi.",
            "Uzmanların sunumlarıyla tarihe ışık tutan bir etkinlik.",
            "Antik dünyanın gizemlerini keşfetmek için eşsiz bir fırsat."
        ],
        "Tarihi Yürüyüş": [
            "Tarihi yerleri keşfederek geçmişe bir yolculuk yapın.",
            "Rehber eşliğinde unutulmaz bir yürüyüş deneyimi.",
            "Yerel tarihin detaylarını öğrenmek isteyenler için keyifli bir etkinlik."
        ],
        "Tarihi Keşif Turu": [
            "Tarihi eserleri ve önemli mekanları ziyaret ederek bilgi edinin.",
            "Geçmişin izlerini sürmek için rehberli bir tur.",
            "Tarihi öğrenirken keyifli bir zaman geçirin."
        ],
        "Geçmişin İzinde": [
            "Geçmişin hikayelerini keşfetmek için uzmanlarla buluşun.",
            "Tarihi belgeler ve objelerle dolu bir sergi.",
            "Tarihi derinlemesine incelemek isteyenler için bir etkinlik."
        ]
    }

}

# Daha fazlasını eklemek istersen, her ilgi alanı ve etkinlik için aynı yapıyı kullanabilirsin.
cinsiyetler = ["Erkek", "Kadın"]

# Popüler e-posta uzantıları
eposta_uzantilari = ["@gmail.com", "@yahoo.com", "@outlook.com"]


# Database için örnek veri seti oluşturmaya yarayacak fonksiyonları içerir
def uretKullanici():
    # Rastgele seçim
    secilen_cinsiyet = random.choice(cinsiyetler)
    if secilen_cinsiyet == "Erkek":
        ad = random.choice(erkek_isimleri)
        profil_binary_data = random.choice(erkek_profiller)
    else:
        ad = random.choice(kadin_isimleri)
        profil_binary_data = random.choice(kadin_profiller)

    soyad = random.choice(turkiye_soyadlar)

    # Kullanıcı adı oluşturma seçenekleri
    secenekler = [
        lambda: f"{ad[:2].lower()}{soyad.lower()}{random.randint(1, 99)}",
        lambda: f"{soyad[:3].capitalize()}{ad[-2:].upper()}{random.randint(10, 99)}",
        lambda: f"{soyad[:3].lower()}{ad[:2].lower()}{random.randint(10, 99)}",
        lambda: f"{ad.capitalize()}{random.randint(1, 9)}{soyad.lower()[:3]}",
        lambda: f"{ad.lower()}{random.randint(100, 999)}{soyad[:2].lower()}",
        lambda: f"{ad[:3].lower()}{soyad[:3].lower()}",
        lambda: f"{ad.capitalize()}{soyad.capitalize()}{random.randint(10, 99)}",
        lambda: f"{ad[:2].upper()}{soyad[:3].lower()}{random.randint(1, 99)}",
        lambda: f"{soyad.capitalize()}{ad[:3].capitalize()}",
        lambda: f"{ad.lower()[:3]}{random.randint(1, 99)}{soyad[:2].upper()}",
        lambda: f"{ad[:2].lower()}{soyad[:2].upper()}{random.randint(10, 99)}",
        lambda: f"{soyad[:3].lower()}{random.randint(100, 999)}{ad[:2].lower()}",
        lambda: f"{ad[:3].capitalize()}{soyad[:3].lower()}",
    ]

    # Rastgele bir uzantı seç
    secilen_uzanti = random.choice(eposta_uzantilari)

    # Rastgele 3 ile 6 arasında ilgi alanı seç
    secilen_ilgi_alanlari = random.sample(ilgi_alanlari, random.randint(3, 6))

    # Seçilen ilgi alanlarını virgülle ayrılmış string haline getir
    ilgi_alanlari_string = ",".join(secilen_ilgi_alanlari)

    # Rastgele bir şehir seç
    secilen_sehir = random.choice(sehirler)

    # Türkiye telefon numarası formatı: 05xxxxxxxxx
    # 5 ile başlayan mobil numara (mobil numara başı 05x)
    telefon_numarasi = f"05{random.randint(100000000, 999999999)}"

    # 1 Ocak 1970 ve 31 Aralık 2007 tarihlerini belirleyelim
    baslangic_tarihi = datetime(1970, 1, 1)
    bitis_tarihi = datetime(2007, 12, 31)

    # Rastgele bir tarih seçmek için iki tarih arasındaki farkı hesapla
    tarih_farki = (bitis_tarihi - baslangic_tarihi).days

    # Farklı gün sayısından rastgele bir gün ekle
    rastgele_gun = random.randint(0, tarih_farki)
    rastgele_tarih = baslangic_tarihi + timedelta(days=rastgele_gun)

    # Rastgele kullanıcı adı seçimi
    kullanici_adi = random.choice(secenekler)()
    # Türkçe karakterleri normalleştir ve yalnızca izin verilen karakterleri bırak
    kullanici_adi = ''.join(
        c for c in unicodedata.normalize('NFD', kullanici_adi)
        if unicodedata.category(c) != 'Mn'
    )  # Türkçe karakterleri sadeleştirir
    kullanici_adi = re.sub(r'[^a-zA-Z0-9]', '', kullanici_adi)  # Geçersiz karakterleri kaldırır

    eposta_isim = random.choice(secenekler)()
    eposta = f"{eposta_isim}{secilen_uzanti}"

    # Şifre uzunluğunu rastgele seç (8 ile 24 arasında)
    sifre_uzunlugu = random.randint(8, 24)

    ozel_karakterler = "@$!%*?&"
    turkce_karakterler = "çşğüöıÇŞĞÜÖİ"
    # İlgi alanlarındaki boşlukları kaldır veya alt çizgi ile değiştir
    temizlenmis_ilgi_alanlari = [
        ilgi.replace(" ", "_") for ilgi in secilen_ilgi_alanlari
    ]
    # Şifre oluşturma seçenekleri
    sifre_secenekler = [
        # Adın baş harfi büyük, soyadın ilk 2 harfi küçük, rastgele sayı
        lambda: f"{ad[0].upper()}{soyad[:2].lower()}{random.randint(10, 99)}",
        # Adın ilk 3 harfi, doğum yılının son iki hanesi, rastgele özel karakter
        lambda: f"{ad[:3].capitalize()}{int(rastgele_tarih.strftime("%Y%m%d")) % 100}{random.choice(ozel_karakterler)}",
        # Soyad büyük harflerle başlar, ardından konumun ilk 3 harfi küçük
        lambda: f"{soyad.capitalize()}{secilen_sehir[:3].lower()}{random.randint(10, 99)}",
        # İlgi alanlarından bir kelime, adın baş harfi ve rastgele sayı
        lambda: f"{random.choice(temizlenmis_ilgi_alanlari)}{ad[0].upper()}{random.randint(100, 999)}",
        # Adın tamamı küçük, konum baş harfi büyük, rastgele özel karakter ve sayı
        lambda: f"{ad.lower()}{secilen_sehir[0].upper()}{random.choice(ozel_karakterler)}{random.randint(1, 9)}",
        # Adın baş harfi büyük, soyadın baş harfi büyük, doğum gününün günü ve Türkçe karakter
        lambda: f"{ad.capitalize()}{soyad.capitalize()}{random.randint(1, 28):02}{random.choice(turkce_karakterler)}",
        # İlgi alanlarından biri, adın ilk iki harfi büyük ve rastgele sayı
        lambda: f"{random.choice(temizlenmis_ilgi_alanlari)}{ad[:2].upper()}{random.randint(10, 99)}",
        # Soyadın tamamı büyük, ardından doğum gününün ayı ve rastgele sayı
        lambda: f"{soyad.upper()}{random.randint(1, 12):02}{random.randint(10, 99)}",
        # Adın ilk harfi, soyadın tamamı, konumun ilk iki harfi ve rastgele sayı
        lambda: f"{ad[:1].upper()}{soyad.lower()}{secilen_sehir[:2].lower()}{random.randint(100, 999)}",
        # Konum ve ilgi alanlarından biriyle kişisel bir karışım
        lambda: f"{secilen_sehir[:3].lower()}{random.choice(temizlenmis_ilgi_alanlari).capitalize()}{random.randint(10, 99)}",
    ]

    # Rastgele bir seçenek seç ve şifre oluştur
    sifre = random.choice(sifre_secenekler)()

    # Eğer şifre uzunluk sınırına uymuyorsa, uygun olacak şekilde ayarla
    if len(sifre) < 8:
        sifre += ''.join(random.choices(string.ascii_letters + string.digits, k=(8 - len(sifre))))
    elif len(sifre) > 24:
        sifre = sifre[:24]

    bilgiler = (99999, kullanici_adi, sifre, eposta, secilen_sehir, ilgi_alanlari_string, ad, soyad,
                rastgele_tarih.strftime("%Y-%m-%d"), secilen_cinsiyet, telefon_numarasi, profil_binary_data)
    uretilen_user: Siniflar.Kullanici = Siniflar.Kullanici(*bilgiler)
    Database.addKullanici(uretilen_user)



# Etkinlik oluşturma fonksiyonu
def uretEtkinlik():
    baslangic_tarihi = datetime(2015, 1, 1)
    bitis_tarihi = datetime(2028, 12, 31)

    # Rastgele bir tarih seçmek için iki tarih arasındaki farkı hesapla
    tarih_farki = (bitis_tarihi - baslangic_tarihi).days

    # Farklı gün sayısından rastgele bir gün ekle
    rastgele_gun = random.randint(0, tarih_farki)

    saat = random.randint(10, 22)  # 10 ve 22 arasında saat seçimi
    dakika = random.choice([0, 15, 30, 45])  # Dakikalar 0, 15, 30, 45


    ilgi_alani = random.choice(ilgi_alanlari)

    # Gereken değişkenlerin son hali
    ID = 99999
    kategori = Fonksiyonlar.ilgi_alani_kategorisi(ilgi_alani, kategoriler)  # ilgi alanına ait kategorilerden seçiyor
    etkinlik_adi = random.choice(etkinlik_isimleri[ilgi_alani])
    etkinlik_aciklama = random.choice(etkinlik_aciklamalari[ilgi_alani][etkinlik_adi])
    rastgele_tarih = baslangic_tarihi + timedelta(days=rastgele_gun)
    etkinlik_saat = f"{saat:02d}:{dakika:02d}"  # Saat formatı: HH:MM
    etkinlik_suresi = random.randint(1, 4)  # 1 ile 4 saat arasında rastgele süre seçimi
    etkinlik_konum = random.choice(sehirler)
    etkinlik_fotograf = random.choice(ilgi_alani_resimleri[ilgi_alani])
    bilgiler = (ID, etkinlik_adi, etkinlik_aciklama, rastgele_tarih.strftime("%Y-%m-%d"),
                etkinlik_saat, etkinlik_suresi, etkinlik_konum, kategori, etkinlik_fotograf)
    newEtkinlik: Siniflar.Etkinlik = Siniflar.Etkinlik(*bilgiler)
    Database.addEtkinlik(newEtkinlik)
    etkinlik_ID = Database.getLastAddedEtkinlikID()
    if etkinlik_ID:
        uretOlusturan(etkinlik_ID, rastgele_tarih)
        Database.updateEtkinlikOnay(Siniflar.EtkinlikOnay(True, etkinlik_ID))  # Etkinliği onaylar
        katilimci_sayisi = random.randint(15, 95)
        for i in range(katilimci_sayisi):
            uretKatilimci(etkinlik_ID, rastgele_tarih)
        uretMesajlar(etkinlik_ID)


# Etkinlik oluşturan oluşturma
def uretOlusturan(etkinlik_ID, etkinlik_Tarih):
    # Rastgele bir kullanıcı bilgisi al
    kullanici_bilgiler = Database.getRandomUser()

    if kullanici_bilgiler:
        kullanici_ID = kullanici_bilgiler[0]
        kullanici_dogum_tarih = kullanici_bilgiler[8]  # 8. indeksin doğum tarihi olduğunu varsayıyoruz

        # Kullanıcının doğum tarihi ile etkinlik tarihi arasında farkı hesapla
        dogum_tarih = datetime.strptime(kullanici_dogum_tarih, "%Y-%m-%d")

        # Eğer etkinlik_Tarih bir datetime nesnesiyse, strptime kullanmaya gerek yok
        if isinstance(etkinlik_Tarih, str):
            etkinlik_tarih = datetime.strptime(etkinlik_Tarih, "%Y-%m-%d")
        else:
            etkinlik_tarih = etkinlik_Tarih  # Zaten datetime nesnesi ise olduğu gibi kullan

        # Yaş farkını hesapla
        yas_farki = (etkinlik_tarih - dogum_tarih).days // 365  # Yaklaşık yıl farkı

        # Eğer yaş farkı 16 yıl ise, oluşturan işlemi yapılacak
        if yas_farki >= 16:
            newOlusturan = Siniflar.Olusturan(kullanici_ID, etkinlik_ID)
            Database.addOlusturan(newOlusturan)
            # print(f"Etkinlik ID {etkinlik_ID} için Oluşturan işlemi başarıyla tamamlandı.")
        else:
            # print("Kullanıcının yaşı etkinlik için yeterli değil. Yeni bir kullanıcı seçiliyor.")
            uretOlusturan(etkinlik_ID, etkinlik_Tarih)  # Tekrar rastgele kullanıcı seç
    else:
        print("Rastgele kullanıcı bulunamadı.")


# Etkinlik katılımcısı oluşturma
def uretKatilimci(etkinlik_ID, etkinlik_Tarih):
    # Rastgele bir kullanıcı bilgisi al
    kullanici_bilgiler = Database.getRandomUser()

    if kullanici_bilgiler:
        kullanici_ID = kullanici_bilgiler[0]
        kullanici_dogum_tarih = kullanici_bilgiler[8]  # 8. indeksin doğum tarihi olduğunu varsayıyoruz

        # Etkinliğin oluşturucusunu kontrol et
        olusturan_bilgiler = Database.getOlusturan_ByEtkinlikID(etkinlik_ID)  # Etkinlik ID'sine göre oluşturan kişiyi al
        if olusturan_bilgiler and olusturan_bilgiler[0] == kullanici_ID:
            # print("Kullanıcı etkinliği oluşturan kişi, yeni bir kullanıcı seçiliyor.")
            uretKatilimci(etkinlik_ID, etkinlik_Tarih)  # Tekrar rastgele kullanıcı seç
            return

        # Kullanıcının doğum tarihi ile etkinlik tarihi arasında farkı hesapla
        dogum_tarih = datetime.strptime(kullanici_dogum_tarih, "%Y-%m-%d")

        # Eğer etkinlik_Tarih bir datetime nesnesiyse, strptime kullanmaya gerek yok
        if isinstance(etkinlik_Tarih, str):
            etkinlik_tarih = datetime.strptime(etkinlik_Tarih, "%Y-%m-%d")
        else:
            etkinlik_tarih = etkinlik_Tarih  # Zaten datetime nesnesi ise olduğu gibi kullan

        # Yaş farkını hesapla
        yas_farki = (etkinlik_tarih - dogum_tarih).days // 365  # Yaklaşık yıl farkı

        # Eğer yaş farkı 16 yıl ise, katılımcı işlemi yapılacak
        if yas_farki >= 16:
            newKatilimci = Siniflar.Katilimci(kullanici_ID, etkinlik_ID)
            Database.addKatilimci(newKatilimci)
            # print(f"Etkinlik ID {etkinlik_ID} için Katılımcı başarıyla eklendi.")
        else:
            # print("Kullanıcının yaşı etkinlik için yeterli değil. Yeni bir kullanıcı seçiliyor.")
            uretKatilimci(etkinlik_ID, etkinlik_Tarih)  # Tekrar rastgele kullanıcı seç
    else:
        print("Rastgele kullanıcı bulunamadı.")

# Etkinliğe katılan için mesaj üretme
def uretMesajlar(etkinlik_id: int):
    """
    Belirtilen etkinlik ID'sine göre mesajları oluşturup gönderir.
    :param etkinlik_id: Etkinlik ID'si
    """
    # Etkinliği getir
    etkinlik_data = Database.searchEtkinlik_ByID(etkinlik_id)
    if not etkinlik_data:
        print("Etkinlik bulunamadı, işlem durduruldu.")
        return False

    # Etkinlik bilgilerini çöz
    etkinlik = Siniflar.Etkinlik(
        ID=etkinlik_data[0],
        etkinlik_adi=etkinlik_data[1],
        aciklama=etkinlik_data[2],
        tarih=etkinlik_data[3],
        saat=etkinlik_data[4],
        etkinlik_suresi=etkinlik_data[5],
        konum=etkinlik_data[6],
        kategori=etkinlik_data[7],
    )

    # Katılımcıları getir
    katilimci_listesi = Database.getAllKatilimci_ByEtkinlikID(etkinlik_id)
    if not katilimci_listesi:
        print("Etkinliğe ait katılımcı bulunamadı, işlem durduruldu.")
        return False

    # Katılımcı ID'lerini listele
    katilimci_ids = [katilimci[0] for katilimci in katilimci_listesi]

    # Etkinlik zaman hesaplamaları
    baslangic_tarihi = datetime.strptime(etkinlik.get_tarih(), "%Y-%m-%d")
    baslangic_saati = datetime.strptime(etkinlik.get_saat(), "%H:%M").time()
    baslangic_zamani = datetime.combine(baslangic_tarihi, baslangic_saati)
    bitis_zamani = baslangic_zamani + timedelta(hours=etkinlik.get_etkinlik_suresi())

    # Etkinlik Sonrası Mesaj Örnekleri
    mesaj_ornekleri_sonrasi = [
        "Etkinlik gerçekten unutulmazdı, teşekkür ederim!",
        "Harika bir etkinlikti, emeği geçen herkese teşekkürler.",
        "Bu etkinlik sayesinde çok şey öğrendim, organizasyon ekibine tebrikler!",
        "Yeni insanlarla tanışmak ve güzel anılar biriktirmek harikaydı.",
        "Katıldığım en güzel etkinliklerden biriydi, devamını sabırsızlıkla bekliyorum.",
        "Etkinlikteki samimiyet ve enerji gerçekten çok iyiydi.",
        "Bu etkinliği kaçırmadığım için çok mutluyum!",
        "İlginç konuşmalar ve harika insanlar bir aradaydı, teşekkürler!",
        "Etkinlikte kendimi çok iyi hissettim, umarım tekrar görüşürüz.",
        "Organizasyon harikaydı, herkes çok ilgiliydi.",
        "Böyle etkinliklerin düzenlenmesi çok güzel, emeği geçenlere teşekkürler.",
        "Bugünkü etkinlik hayatımda yeni bir sayfa açmamı sağladı.",
        "Etkinlikte aldığım ilham, uzun süre benimle olacak.",
        "Bu etkinlikten gerçekten çok şey öğrendim.",
        "Sıradaki etkinliği dört gözle bekliyorum!",
        "Etkinlikte herkesin gösterdiği çaba görülmeye değerdi.",
        "Harika bir deneyimdi, emeği geçen herkesin ellerine sağlık.",
        "Etkinlikten edindiğim bilgiler bana çok şey kattı.",
        "Bu etkinlikte olmak benim için büyük bir şanstı.",
        "Muhteşem bir etkinlikti, tekrar görüşmek dileğiyle!",
        "Etkinlikteki atmosfer mükemmeldi, teşekkürler!",
        "Bu tarz etkinliklerin daha sık yapılmasını isterim.",
        "Organizasyon çok profesyoneldi, tekrar teşekkür ederim.",
        "Katıldığım için kendimi çok şanslı hissediyorum.",
        "Böylesine güzel bir organizasyonda yer almak büyük bir keyifti.",
        "Etkinlik sonrası herkesin düşüncelerini öğrenmek isterim.",
        "Bu etkinlik benim için unutulmaz bir deneyim oldu.",
        "Harika bir gün geçirdim, organizasyonu yapan herkese teşekkür ederim.",
        "Etkinlikteki enerjiyi ve motivasyonu hiç unutmayacağım."
    ]

    # Etkinlik Öncesi Mesaj Örnekleri
    mesaj_ornekleri_oncesi = [
        "Etkinlik için sabırsızlanıyorum, harika bir gün olacak gibi!",
        "Bugünkü etkinlikte herkesle tanışmayı dört gözle bekliyorum.",
        "Etkinlik programı çok ilgi çekici görünüyor, harika bir gün olacak.",
        "Katılacağım için çok heyecanlıyım!",
        "Etkinlikte çok şey öğreneceğimden eminim, görüşmek üzere!",
        "Bugünkü etkinlik için hazırlıklar tamam, sabırsızlanıyorum.",
        "Etkinlikte görüşmek için sabırsızlanıyorum!",
        "Harika bir etkinlik olacağından hiç şüphem yok.",
        "Etkinlik programına bayıldım, orada olacağım için çok mutluyum.",
        "Bugünkü etkinlik hayatımda bir dönüm noktası olabilir.",
        "Etkinlik öncesi enerjimi toparlıyorum, görüşmek üzere!",
        "Katılımcılarla tanışmak için sabırsızlanıyorum.",
        "Etkinlikteki konuşmacıları dinlemek için heyecanlıyım.",
        "Bu etkinlikten beklentilerim oldukça yüksek, görüşmek dileğiyle!",
        "Hazırlıklarımı tamamladım, etkinlik için hazır hissediyorum.",
        "Bugün yepyeni bilgilerle dolu bir gün olacak gibi.",
        "Etkinlik günü nihayet geldi, harika bir organizasyon bekliyorum.",
        "Etkinlik öncesi herkese başarılar dilerim!",
        "Konuşmacılardan biriyle tanışmayı özellikle istiyorum.",
        "Bugünkü etkinlikte güzel dostluklar kurulacak gibi hissediyorum.",
        "Etkinlik başlamak üzere, büyük bir heyecanla bekliyorum.",
        "Katılacağım etkinliklerden biri olacağına eminim!",
        "Programı inceledim, bugün gerçekten dolu dolu bir gün olacak.",
        "Etkinlik için enerjimi topladım, görüşmek dileğiyle.",
        "Bugün yeni şeyler öğrenmek için sabırsızlanıyorum.",
        "Etkinlikten sonra güzel anılarla döneceğimden eminim.",
        "Hazırlıklar tamam, bugün harika bir gün olacak.",
        "Bu etkinlik sayesinde yeni şeyler öğrenmek için sabırsızlanıyorum.",
        "Herkesle buluşmak için sabırsızlanıyorum, görüşmek üzere!"
    ]

    # Rastgele 15-75 katılımcı seç
    secilen_katilimcilar = random.sample(katilimci_ids, k=min(len(katilimci_ids), random.randint(15, 75)))

    for katilimci_id in secilen_katilimcilar:
        # Katılımcıyı getir
        katilimci = Database.searchKullanici_ByID(katilimci_id)
        if not katilimci:
            print(f"Kullanıcı ID {katilimci_id} bulunamadı, atlanıyor.")
            continue

        # Gönderim tarihini belirle
        if random.choice([True, False]):  # %50 ihtimalle etkinlik öncesi mesaj
            start_date = baslangic_zamani - timedelta(days=365)
            end_date = baslangic_zamani - timedelta(seconds=1)
            mesaj_metni = random.choice(mesaj_ornekleri_oncesi)
        else:  # %50 ihtimalle etkinlik sonrası mesaj
            start_date = bitis_zamani
            end_date = bitis_zamani + timedelta(days=1)
            mesaj_metni = random.choice(mesaj_ornekleri_sonrasi)

        """Belirtilen iki datetime arasında rastgele bir tarih üretir."""
        delta = (end_date - start_date).total_seconds()
        random_seconds = random.randint(0, int(delta))
        gonderim_zamani = start_date + timedelta(seconds=random_seconds)

        # Mesaj nesnesi oluştur
        mesaj = Siniflar.Mesaj(
            mesaj_id=None,  # Veritabanı otomatik olarak ayarlayacak
            gonderici_id=katilimci_id,
            alici_id=etkinlik.get_ID(),
            mesaj_metni=mesaj_metni,
            gonderim_zamani=gonderim_zamani.strftime("%Y-%m-%d %H:%M:%S")
        )

        # Mesajı veritabanına ekle
        if Database.addMesaj(mesaj):
            print(f"Kullanıcı {katilimci_id} için mesaj başarıyla eklendi.")
        else:
            print(f"Kullanıcı {katilimci_id} için mesaj eklenirken hata oluştu.")


# Veri üretme fonksiyonu
def veriUret():
    # Hazır bilgiler
    for ilgi_alan in ilgi_alanlari:
        Database.addIlgiAlani(ilgi_alan)

    for ilgi_alan, kategori in kategoriler.items():
        for kategori_bilgi in kategori:
            Database.addKategori(ilgi_alan, kategori_bilgi)

    for sehir in sehirler:
        Database.addKonum(sehir)

    # Üretilen bilgiler
    for i in range(900):
        print(f"{i + 1:<3}", end=" ")
        uretKullanici()

    for i in range(110):
        print(f"{i + 1:<3}", end=" ")
        uretEtkinlik()


#veriUret()
