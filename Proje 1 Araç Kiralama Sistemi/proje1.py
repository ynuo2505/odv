import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget, \
    QCalendarWidget, QTimeEdit, QComboBox, QMessageBox, QDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap
import re

class Arac:
    def __init__(self, arac_id, marka, model, yil, kiralama_durumu):
        self.arac_id = arac_id
        self.marka = marka
        self.model = model
        self.yil = yil
        self.kiralama_durumu = kiralama_durumu

    def arac_durumu_guncelle(self, yeni_durum):
        self.kiralama_durumu = yeni_durum

class Musteri:
    def __init__(self, ad, soyad, eposta, telefon, adres):
        self.ad = ad
        self.soyad = soyad
        self.eposta = eposta
        self.telefon = telefon
        self.adres = adres

class Kiralama:
    def __init__(self):
        self.kiralanan_arac = None
        self.musteri = None

    def kiralama_yap(self, musteri, arac):
        if arac.kiralama_durumu == "Müsait":
            self.kiralanan_arac = arac
            self.musteri = musteri
            arac.arac_durumu_guncelle("Kiralandı")
            print(f"{musteri.ad} {musteri.soyad}, {arac.marka} {arac.model} aracı kiraladı.")
        else:
            print("Bu araç şu anda kiralanamaz.")

    def kiralama_iptal_et(self):
        if self.kiralanan_arac:
            self.kiralanan_arac.arac_durumu_guncelle("Müsait")
            print(f"{self.musteri.ad} {self.musteri.soyad}, kiralama işlemini iptal etti.")
            self.kiralanan_arac = None
            self.musteri = None
        else:
            print("Henüz bir araç kiralama işlemi gerçekleştirilmemiş.")

    def kiralama_bilgisi(self):
        if self.kiralanan_arac and self.musteri:
            print(
                f"{self.musteri.ad} {self.musteri.soyad} tarafından {self.kiralanan_arac.marka} {self.kiralanan_arac.model} aracı kiralandı.")
        else:
            print("Henüz bir kiralama işlemi gerçekleştirilmemiş.")

class PreLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ön Giriş Ekranı")
        self.setGeometry(200, 200, 400, 600)

        # Arka plan resmi
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 400, 600)
        self.background_label.setPixmap(QPixmap("background.jpg"))  # Arka plan resmi dosya adı

        self.label_alis_yeri = QLabel("Alış Yeri:", self)
        self.label_alis_yeri.setGeometry(50, 50, 100, 30)
        self.combo_alis_yeri = QComboBox(self)
        self.combo_alis_yeri.setGeometry(150, 50, 200, 30)

        self.label_birak_yeri = QLabel("Bırakış Yeri:", self)
        self.label_birak_yeri.setGeometry(50, 100, 100, 30)
        self.combo_birak_yeri = QComboBox(self)
        self.combo_birak_yeri.setGeometry(150, 100, 200, 30)

        self.label_alis_tarihi = QLabel("Alış Tarihi:", self)
        self.label_alis_tarihi.setGeometry(50, 150, 100, 30)
        self.calendar_alis = QCalendarWidget(self)
        self.calendar_alis.setGeometry(150, 150, 200, 150)

        self.label_alis_saati = QLabel("Alış Saati:", self)
        self.label_alis_saati.setGeometry(50, 300, 100, 30)
        self.timeedit_alis = QTimeEdit(self)
        self.timeedit_alis.setGeometry(150, 300, 100, 30)

        self.label_donus_tarihi = QLabel("Dönüş Tarihi:", self)
        self.label_donus_tarihi.setGeometry(50, 350, 100, 30)
        self.calendar_donus = QCalendarWidget(self)
        self.calendar_donus.setGeometry(150, 350, 200, 150)

        self.label_donus_saati = QLabel("Dönüş Saati:", self)
        self.label_donus_saati.setGeometry(50, 500, 100, 30)
        self.timeedit_donus = QTimeEdit(self)
        self.timeedit_donus.setGeometry(150, 500, 100, 30)

        self.btn_kirala = QPushButton("Kirala", self)
        self.btn_kirala.setGeometry(150, 550, 100, 30)
        self.btn_kirala.clicked.connect(self.kirala)

        self.btn_giris = QPushButton("Giriş Yap", self)
        self.btn_giris.setGeometry(270, 550, 100, 30)
        self.btn_giris.clicked.connect(self.giris_ekranina_yonlendir)

        # Türkiye'nin tüm şehirlerini içeren liste
        tum_sehirler = [
            "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir",
            "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli",
            "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane",
            "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli",
            "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş",
            "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat",
            "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman",
            "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye",
            "Düzce"
        ]

        # Alış ve bırakış yerlerini doldurma
        self.combo_alis_yeri.addItems(tum_sehirler)
        self.combo_birak_yeri.addItems(tum_sehirler)

    def kirala(self):
        # Alış ve bırakış yerleri seçildi mi kontrol et
        alis_yeri = self.combo_alis_yeri.currentText()
        birak_yeri = self.combo_birak_yeri.currentText()
        if not alis_yeri or not birak_yeri:
            QMessageBox.warning(self, "Uyarı", "Lütfen alış ve bırakış yerlerini seçiniz!")
            return

        # Tarih ve saatleri kontrol et
        alis_tarihi = self.calendar_alis.selectedDate().toString("yyyy-MM-dd")
        donus_tarihi = self.calendar_donus.selectedDate().toString("yyyy-MM-dd")
        alis_saati = self.timeedit_alis.time().toString("hh:mm")
        donus_saati = self.timeedit_donus.time().toString("hh:mm")
        if alis_tarihi >= donus_tarihi:
            QMessageBox.warning(self, "Uyarı", "Dönüş tarihi alış tarihinden ileri bir tarih olmalıdır!")
            return
        if alis_tarihi == donus_tarihi and alis_saati >= donus_saati:
            QMessageBox.warning(self, "Uyarı", "Dönüş saati alış saatinden ileri bir saat olmalıdır!")
            return

        # Saatlerin de seçildiğinden emin ol
        if alis_saati == "00:00" or donus_saati == "00:00":
            QMessageBox.warning(self, "Uyarı", "Lütfen alış ve dönüş saatlerini seçiniz!")
            return

        # Diğer alanları da kontrol et ve gerekli işlemleri yap
        QMessageBox.information(self, "KiralaJet- Araç Kiralama Sistemi", "Kiralama işlemini tamamlamak için giriş yapınız!")

    def giris_ekranina_yonlendir(self):
        self.login_window = LoginWindow()
        self.login_window.show()

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("KiralaJet Giriş Ekranı")
        self.setGeometry(300, 300, 400, 200)

        self.label_kullanici_adi = QLabel("E-posta:", self)
        self.label_kullanici_adi.setGeometry(50, 50, 100, 30)
        self.input_kullanici_adi = QLineEdit(self)
        self.input_kullanici_adi.setGeometry(150, 50, 200, 30)

        self.label_sifre = QLabel("Şifre:", self)
        self.label_sifre.setGeometry(50, 100, 100, 30)
        self.input_sifre = QLineEdit(self)
        self.input_sifre.setGeometry(150, 100, 200, 30)
        self.input_sifre.setEchoMode(QLineEdit.Password)

        self.btn_giris = QPushButton("Giriş Yap", self)
        self.btn_giris.setGeometry(150, 150, 100, 30)
        self.btn_giris.clicked.connect(self.giris_yap)

        self.btn_kayit = QPushButton("Kayıt Ol", self)
        self.btn_kayit.setGeometry(270, 150, 100, 30)
        self.btn_kayit.clicked.connect(self.kayit_ol)

    def giris_yap(self):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        email = self.input_kullanici_adi.text()
        password = self.input_sifre.text()

        if not re.match(email_regex, email):
            QMessageBox.warning(self, "Uyarı", "Geçerli bir e-posta adresi giriniz!")
            return

        if len(password) < 8:
            QMessageBox.warning(self, "Uyarı", "Şifre en az 8 karakter uzunluğunda olmalıdır!")
            return

        # E-posta ve şifre doğru girildiğinde müşteri bilgilerini kontrol et
        for musteri in kayitli_musteriler:
            if musteri.eposta == email and musteri.sifre == password:
                self.musteri = musteri
                self.arac_listesi = [
            Arac(1, "Volvo", "XC90", 2020, "Müsait"),
            Arac(2, "Volvo", "XC60", 2019, "Müsait"),
            Arac(3, "Volvo", "V90", 2018, "Müsait"),
            Arac(4, "Volvo", "S90", 2017, "Müsait"),
            Arac(5, "Volvo", "XC40", 2016, "Müsait"),
            Arac(6, "Volkswagen", "Passat", 2021, "Müsait"),
            Arac(7, "Volkswagen", "Tiguan", 2020, "Müsait"),
            Arac(8, "Volkswagen", "Golf", 2019, "Müsait"),
            Arac(9, "Volkswagen", "T-Roc", 2018, "Müsait"),
            Arac(10, "Volkswagen", "Arteon", 2017, "Müsait"),
            Arac(11, "BMW", "3 Serisi", 2022, "Müsait"),
            Arac(12, "BMW", "5 Serisi", 2021, "Müsait"),
            Arac(13, "BMW", "X3", 2020, "Müsait"),
            Arac(14, "BMW", "X5", 2019, "Müsait"),
            Arac(15, "BMW", "7 Serisi", 2018, "Müsait"),
            Arac(16, "Audi", "A4", 2022, "Müsait"),
            Arac(17, "Audi", "A5", 2021, "Müsait"),
            Arac(18, "Audi", "Q5", 2020, "Müsait"),
            Arac(19, "Audi", "Q3", 2019, "Müsait"),
            Arac(20, "Audi", "A6", 2018, "Müsait"),
            Arac(21, "Mercedes", "C Serisi", 2023, "Müsait"),
            Arac(22, "Mercedes", "E Serisi", 2022, "Müsait"),
            Arac(23, "Mercedes", "GLC", 2021, "Müsait"),
            Arac(24, "Mercedes", "GLE", 2020, "Müsait"),
            Arac(25, "Mercedes", "S Serisi", 2019, "Müsait"),
            Arac(26, "Opel", "Astra", 2022, "Müsait"),
            Arac(27, "Opel", "Corsa", 2021, "Müsait"),
            Arac(28, "Opel", "Crossland X", 2020, "Müsait"),
            Arac(29, "Opel", "Mokka X", 2019, "Müsait"),
            Arac(30, "Opel", "Insignia", 2018, "Müsait"),
            Arac(31, "Toyota", "Corolla", 2022, "Müsait"),
            Arac(32, "Toyota", "C-HR", 2021, "Müsait"),
            Arac(33, "Toyota", "RAV4", 2020, "Müsait"),
            Arac(34, "Toyota", "Yaris", 2019, "Müsait"),
            Arac(35, "Toyota", "Camry", 2018, "Müsait"),
            Arac(36, "Honda", "Civic", 2023, "Müsait"),
            Arac(37, "Honda", "HR-V", 2022, "Müsait"),
            Arac(38, "Honda", "CR-V", 2021, "Müsait")
             ]

                self.arac_kiralama_sayfasi = AracKiralamaSayfasi(self.musteri, self.arac_listesi)
                self.arac_kiralama_sayfasi.show()
                self.close()
                return

        QMessageBox.warning(self, "Uyarı", "Geçersiz e-posta veya şifre!")

        # E-posta ve şifre doğru girildi, müşteri bilgileriyle araç listesinin bulunduğu sayfaya yönlendir
        self.musteri = Musteri("Ahmet", "Yılmaz", "ahmet@example.com", "123456789", "İstanbul")
        self.arac_listesi = [
            Arac(1, "Volvo", "XC90", 2020, "Müsait"),
            Arac(2, "Volvo", "XC60", 2019, "Müsait"),
            Arac(3, "Volvo", "V90", 2018, "Müsait"),
            Arac(4, "Volvo", "S90", 2017, "Müsait"),
            Arac(5, "Volvo", "XC40", 2016, "Müsait"),
            Arac(6, "Volkswagen", "Passat", 2021, "Müsait"),
            Arac(7, "Volkswagen", "Tiguan", 2020, "Müsait"),
            Arac(8, "Volkswagen", "Golf", 2019, "Müsait"),
            Arac(9, "Volkswagen", "T-Roc", 2018, "Müsait"),
            Arac(10, "Volkswagen", "Arteon", 2017, "Müsait"),
            Arac(11, "BMW", "3 Serisi", 2022, "Müsait"),
            Arac(12, "BMW", "5 Serisi", 2021, "Müsait"),
            Arac(13, "BMW", "X3", 2020, "Müsait"),
            Arac(14, "BMW", "X5", 2019, "Müsait"),
            Arac(15, "BMW", "7 Serisi", 2018, "Müsait"),
            Arac(16, "Audi", "A4", 2022, "Müsait"),
            Arac(17, "Audi", "A5", 2021, "Müsait"),
            Arac(18, "Audi", "Q5", 2020, "Müsait"),
            Arac(19, "Audi", "Q3", 2019, "Müsait"),
            Arac(20, "Audi", "A6", 2018, "Müsait"),
            Arac(21, "Mercedes", "C Serisi", 2023, "Müsait"),
            Arac(22, "Mercedes", "E Serisi", 2022, "Müsait"),
            Arac(23, "Mercedes", "GLC", 2021, "Müsait"),
            Arac(24, "Mercedes", "GLE", 2020, "Müsait"),
            Arac(25, "Mercedes", "S Serisi", 2019, "Müsait"),
            Arac(26, "Opel", "Astra", 2022, "Müsait"),
            Arac(27, "Opel", "Corsa", 2021, "Müsait"),
            Arac(28, "Opel", "Crossland X", 2020, "Müsait"),
            Arac(29, "Opel", "Mokka X", 2019, "Müsait"),
            Arac(30, "Opel", "Insignia", 2018, "Müsait"),
            Arac(31, "Toyota", "Corolla", 2022, "Müsait"),
            Arac(32, "Toyota", "C-HR", 2021, "Müsait"),
            Arac(33, "Toyota", "RAV4", 2020, "Müsait"),
            Arac(34, "Toyota", "Yaris", 2019, "Müsait"),
            Arac(35, "Toyota", "Camry", 2018, "Müsait"),
            Arac(36, "Honda", "Civic", 2023, "Müsait"),
            Arac(37, "Honda", "HR-V", 2022, "Müsait"),
            Arac(38, "Honda", "CR-V", 2021, "Müsait")
        ]

        self.arac_kiralama_sayfasi = AracKiralamaSayfasi(self.musteri, self.arac_listesi)
        self.arac_kiralama_sayfasi.show()
        self.close()

    def kayit_ol(self):
        self.kayit_window = KayitWindow()
        self.kayit_window.show()
        self.close()

class KayitWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("KiralaJet Kayıt Ekranı")
        self.setGeometry(300, 300, 400, 350)

        self.label_ad = QLabel("Ad:", self)
        self.label_ad.setGeometry(50, 50, 100, 30)
        self.input_ad = QLineEdit(self)
        self.input_ad.setGeometry(150, 50, 200, 30)

        self.label_soyad = QLabel("Soyad:", self)
        self.label_soyad.setGeometry(50, 100, 100, 30)
        self.input_soyad = QLineEdit(self)
        self.input_soyad.setGeometry(150, 100, 200, 30)

        self.label_eposta = QLabel("E-posta:", self)
        self.label_eposta.setGeometry(50, 150, 100, 30)
        self.input_eposta = QLineEdit(self)
        self.input_eposta.setGeometry(150, 150, 200, 30)

        self.label_telefon = QLabel("Telefon:", self)
        self.label_telefon.setGeometry(50, 200, 100, 30)
        self.input_telefon = QLineEdit(self)
        self.input_telefon.setGeometry(150, 200, 200, 30)

        self.label_sifre = QLabel("Şifre:", self)
        self.label_sifre.setGeometry(50, 250, 100, 30)
        self.input_sifre = QLineEdit(self)
        self.input_sifre.setGeometry(150, 250, 200, 30)
        self.input_sifre.setEchoMode(QLineEdit.Password)

        self.label_adres = QLabel("Adres:", self)
        self.label_adres.setGeometry(50, 300, 100, 30)
        self.input_adres = QLineEdit(self)
        self.input_adres.setGeometry(150, 300, 200, 30)

        self.btn_kaydet = QPushButton("Kaydet", self)
        self.btn_kaydet.setGeometry(150, 350, 100, 30)
        self.btn_kaydet.clicked.connect(self.kaydet)

    def kaydet(self):
        # E-posta formatını kontrol et
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        email = self.input_eposta.text()

        if not re.match(email_regex, email):
            QMessageBox.warning(self, "Uyarı", "Geçerli bir e-posta adresi giriniz!")
            return

        # Telefon numarası formatını kontrol et
        phone_regex = r'^\d{10}$'
        telefon = self.input_telefon.text()

        if not re.match(phone_regex, telefon):
            QMessageBox.warning(self, "Uyarı", "Geçerli bir telefon numarası giriniz! (Örn: 5551234567)")
            return

        # Diğer bilgileri al ve kayıt işlemini tamamla
        ad = self.input_ad.text()
        soyad = self.input_soyad.text()
        adres =  self.input_adres.text()
        sifre = self.input_sifre.text()

        if len(sifre) < 8:
            QMessageBox.warning(self, "Uyarı", "Şifre en az 8 karakter uzunluğunda olmalıdır!")
            return

        musteri = Musteri(ad, soyad, email, telefon, adres)

        QMessageBox.information(self, "Kayıt Başarılı", "Kayıt işlemi başarıyla tamamlandı!")
        self.close()
        # Giriş ekranına yönlendir
        self.giris_ekranina_yonlendir()

    def giris_ekranina_yonlendir(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


class AracKiralamaSayfasi(QMainWindow):
    def __init__(self, musteri, arac_listesi):
        super().__init__()

        self.setWindowTitle("KiralaJet Araç Kiralama Sayfası")
        self.setGeometry(300, 300, 800, 600)

        self.musteri = musteri
        self.arac_listesi = arac_listesi

        self.label_musteri_bilgileri = QLabel(f"Müşteri Bilgileri:\nAd: {self.musteri.ad}\nSoyad: {self.musteri.soyad}\nE-posta: {self.musteri.eposta}\nTelefon: {self.musteri.telefon}\nAdres: {self.musteri.adres}", self)
        self.label_musteri_bilgileri.setGeometry(50, 50, 300, 150)

        self.label_arac_listesi = QLabel("Araç Listesi:", self)
        self.label_arac_listesi.setGeometry(400, 50, 100, 30)

        self.list_arac_listesi = QListWidget(self)
        self.list_arac_listesi.setGeometry(400, 100, 350, 400)
        self.list_arac_listesi.addItem("Marka - Model - Yıl - Durum")
        for arac in self.arac_listesi:
            self.list_arac_listesi.addItem(
                f"{arac.marka} {arac.model} - {arac.yil} - {arac.kiralama_durumu}")

        self.btn_kirala = QPushButton("Seçileni Kirala", self)
        self.btn_kirala.setGeometry(400, 520, 150, 30)
        self.btn_kirala.clicked.connect(self.arac_kirala)

        self.btn_iptal = QPushButton("Seçileni İptal Et", self)
        self.btn_iptal.setGeometry(600, 520, 150, 30)
        self.btn_iptal.clicked.connect(self.arac_iptal)

    def arac_kirala(self):
        secilen_arac_index = self.list_arac_listesi.currentRow() - 1  # Liste başlığı çıkar
        if secilen_arac_index < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir araç seçiniz!")
            return

        secilen_arac = self.arac_listesi[secilen_arac_index]
        kiralama_penceresi = KiralamaPenceresi(self.musteri, secilen_arac)
        kiralama_penceresi.exec_()

    def arac_iptal(self):
        secilen_arac_index = self.list_arac_listesi.currentRow() - 1  # Liste başlığı çıkar
        if secilen_arac_index < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir araç seçiniz!")
            return

        secilen_arac = self.arac_listesi[secilen_arac_index]
        secilen_arac.arac_durumu_guncelle("Müsait")
        QMessageBox.information(self, "İptal Edildi", f"{secilen_arac.marka} {secilen_arac.model} aracı kiralama işlemi iptal edildi.")
        self.list_arac_listesi.clear()
        self.list_arac_listesi.addItem("Marka - Model - Yıl - Durum")
        for arac in self.arac_listesi:
            self.list_arac_listesi.addItem(
                f"{arac.marka} {arac.model} - {arac.yil} - {arac.kiralama_durumu}")


class KiralamaPenceresi(QDialog):
    def __init__(self, musteri, secilen_arac):
        super().__init__()

        self.setWindowTitle("Araç Kiralama")
        self.setGeometry(300, 300, 400, 200)

        self.musteri = musteri
        self.secilen_arac = secilen_arac

        self.label_musteri_bilgileri = QLabel(f"Müşteri Bilgileri:\nAd: {self.musteri.ad}\nSoyad: {self.musteri.soyad}\nE-posta: {self.musteri.eposta}\nTelefon: {self.musteri.telefon}\nAdres: {self.musteri.adres}", self)
        self.label_musteri_bilgileri.setGeometry(50, 50, 300, 150)

        self.label_arac_bilgileri = QLabel(f"Seçilen Araç Bilgileri:\nMarka: {self.secilen_arac.marka}\nModel: {self.secilen_arac.model}\nYıl: {self.secilen_arac.yil}\nDurum: {self.secilen_arac.kiralama_durumu}", self)
        self.label_arac_bilgileri.setGeometry(200, 50, 300, 150)

        self.btn_kirala = QPushButton("Kiralama Yap", self)
        self.btn_kirala.setGeometry(100, 150, 100, 30)
        self.btn_kirala.clicked.connect(self.kirala)

        self.btn_iptal = QPushButton("İptal", self)
        self.btn_iptal.setGeometry(250, 150, 100, 30)
        self.btn_iptal.clicked.connect(self.iptal)

    def kirala(self):
        kiralama = Kiralama()
        kiralama.kiralama_yap(self.musteri, self.secilen_arac)
        self.accept()

    def iptal(self):
        self.reject()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    prelogin_window = PreLoginWindow()
    prelogin_window.show()
    sys.exit(app.exec_())
