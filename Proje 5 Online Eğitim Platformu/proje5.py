import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QLabel, QDialog, QLineEdit, QMessageBox, QComboBox, QDialogButtonBox,
    QCalendarWidget, QListWidget, QTimeEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt, QDate, QTime

class Kurs:
    def __init__(self, adi, egitmenler, icerik):
        self.adi = adi
        self.egitmenler = egitmenler
        self.icerik = icerik

class Egitmen:
    def __init__(self, isim, uzmanlik_alani):
        self.isim = isim
        self.uzmanlik_alani = uzmanlik_alani

class Ogrenci:
    def __init__(self, isim, soyisim, tc, sifre, secilen_ders):
        self.isim = isim
        self.soyisim = soyisim
        self.tc = tc
        self.sifre = sifre
        self.secilen_ders = secilen_ders

class OgretmenKayitPenceresi(QDialog):
    def __init__(self, ogretmen_verileri, kurslar):
        super().__init__()
        self.setWindowTitle("Öğretmen Kayıt")
        self.setFixedSize(400, 300)
        self.ogretmen_verileri = ogretmen_verileri
        self.kurslar = kurslar

        self.layout = QVBoxLayout(self)

        self.label_isim = QLabel("İsim:")
        self.edit_isim = QLineEdit()
        self.layout.addWidget(self.label_isim)
        self.layout.addWidget(self.edit_isim)

        self.label_ders = QLabel("Ders Seçin:")
        self.combo_ders = QComboBox()
        self.combo_ders.addItems(["Matematik", "Fizik", "Kimya", "Biyoloji", "Tarih"])
        self.layout.addWidget(self.label_ders)
        self.layout.addWidget(self.combo_ders)

        self.kayit_button = QPushButton("Kayıt Ol")
        self.kayit_button.clicked.connect(self.kayit_ol)
        self.layout.addWidget(self.kayit_button)

    def kayit_ol(self):
        isim = self.edit_isim.text()
        secilen_ders = self.combo_ders.currentText()

        if not isim:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")
            return

        self.ogretmen_verileri[isim] = Egitmen(isim, secilen_ders)

        # Seçilen dersin hocası olarak ekleniyor
        for kurs in self.kurslar:
            if kurs.adi == secilen_ders:
                kurs.egitmenler.append(Egitmen(isim, secilen_ders))

        QMessageBox.information(self, "Bilgi", "Öğretmen başarıyla kaydedildi.\n\nİsim: {}\nDers: {}".format(isim, secilen_ders))
        self.close()

class KayitPenceresi(QDialog):
    def __init__(self, kayit_verileri):
        super().__init__()
        self.setWindowTitle("Kayıt Ol")
        self.setFixedSize(800, 600)
        self.kayit_verileri = kayit_verileri

        self.layout = QVBoxLayout(self)

        self.label_isim = QLabel("İsim:")
        self.edit_isim = QLineEdit()
        self.layout.addWidget(self.label_isim)
        self.layout.addWidget(self.edit_isim)

        self.label_soyisim = QLabel("Soyisim:")
        self.edit_soyisim = QLineEdit()
        self.layout.addWidget(self.label_soyisim)
        self.layout.addWidget(self.edit_soyisim)

        self.label_tc = QLabel("TC:")
        self.edit_tc = QLineEdit()
        self.layout.addWidget(self.label_tc)
        self.layout.addWidget(self.edit_tc)

        self.label_sifre = QLabel("Şifre:")
        self.edit_sifre = QLineEdit()
        self.edit_sifre.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.label_sifre)
        self.layout.addWidget(self.edit_sifre)

        self.label_sifre_tekrar = QLabel("Şifre Tekrar:")
        self.edit_sifre_tekrar = QLineEdit()
        self.edit_sifre_tekrar.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.label_sifre_tekrar)
        self.layout.addWidget(self.edit_sifre_tekrar)

        self.label_ders = QLabel("Ders Seçin:")
        self.combo_ders = QComboBox()
        self.combo_ders.addItems(["Matematik", "Fizik", "Kimya", "Biyoloji", "Tarih"])
        self.layout.addWidget(self.label_ders)
        self.layout.addWidget(self.combo_ders)

        self.kayit_button = QPushButton("Kayıt Ol")
        self.kayit_button.clicked.connect(self.kayit_ol)
        self.layout.addWidget(self.kayit_button)

    def kayit_ol(self):
        isim = self.edit_isim.text()
        soyisim = self.edit_soyisim.text()
        tc = self.edit_tc.text()
        sifre = self.edit_sifre.text()
        sifre_tekrar = self.edit_sifre_tekrar.text()
        secilen_ders = self.combo_ders.currentText()

        if not isim or not soyisim or not tc or not sifre or not sifre_tekrar:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")
            return

        if tc in self.kayit_verileri:
            QMessageBox.warning(self, "Uyarı", "Bu TC kimlik numarası zaten kullanımda.")
            return

        if sifre != sifre_tekrar:
            QMessageBox.warning(self, "Uyarı", "Girilen şifreler eşleşmiyor.")
            return

        self.kayit_verileri[tc] = Ogrenci(isim, soyisim, tc, sifre, secilen_ders)
        QMessageBox.information(self, "Bilgi", "Kayıt başarıyla oluşturuldu.\n\nİsim: {}\nSoyisim: {}\nTC: {}\nSeçilen Ders: {}".format(isim, soyisim, tc, secilen_ders))
        self.close()

class GirisPenceresi(QDialog):
    def __init__(self, kayit_verileri):
        super().__init__()
        self.setWindowTitle("Giriş Yap")
        self.setFixedSize(800, 600)
        self.kayit_verileri = kayit_verileri

        self.layout = QVBoxLayout(self)

        self.label_isim = QLabel("İsim:")
        self.edit_isim = QLineEdit()
        self.layout.addWidget(self.label_isim)
        self.layout.addWidget(self.edit_isim)

        self.label_soyisim = QLabel("Soyisim:")
        self.edit_soyisim = QLineEdit()
        self.layout.addWidget(self.label_soyisim)
        self.layout.addWidget(self.edit_soyisim)

        self.label_sifre = QLabel("Şifre:")
        self.edit_sifre = QLineEdit()
        self.edit_sifre.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.label_sifre)
        self.layout.addWidget(self.edit_sifre)

        self.giris_button = QPushButton("Giriş Yap")
        self.giris_button.clicked.connect(self.giris_yap)
        self.layout.addWidget(self.giris_button)

    def giris_yap(self):
        isim = self.edit_isim.text()
        soyisim = self.edit_soyisim.text()
        sifre = self.edit_sifre.text()

        for ogrenci in self.kayit_verileri.values():
            if ogrenci.isim == isim and ogrenci.soyisim == soyisim and ogrenci.sifre == sifre:
                self.ogrenci = ogrenci
                self.accept()
                return

        QMessageBox.warning(self, "Uyarı", "Giriş bilgileri geçersiz.")

    def get_ogrenci(self):
        return self.ogrenci


class DerslerPenceresi(QDialog):
    def __init__(self, ogrenci, kurslar):
        super().__init__()
        self.setWindowTitle("Dersler")
        self.setFixedSize(800, 600)
        self.ogrenci = ogrenci
        self.kurslar = kurslar
        self.secilen_gun = None
        self.secilen_saat = None
        self.alinan_dersler = []

        self.layout = QVBoxLayout(self)

        self.label_hosgeldiniz = QLabel(f"Hoş geldiniz, {self.ogrenci.isim} {self.ogrenci.soyisim}")
        self.layout.addWidget(self.label_hosgeldiniz)

        self.label_secilen_ders = QLabel(f"Seçtiğiniz ders: {self.ogrenci.secilen_ders}")
        self.layout.addWidget(self.label_secilen_ders)

        self.label_takvim = QLabel("Takvim")
        self.layout.addWidget(self.label_takvim)

        self.takvim = QCalendarWidget()
        self.takvim.selectionChanged.connect(self.gun_secildi)
        self.layout.addWidget(self.takvim)

        self.label_ogretmenler = QLabel("Öğretmenler Listesi")
        self.layout.addWidget(self.label_ogretmenler)

        self.liste_ogretmenler = QListWidget()
        self.liste_ogretmenler.addItems(self.get_egitmenler_for_ders(self.ogrenci.secilen_ders))
        self.layout.addWidget(self.liste_ogretmenler)

        self.label_saat = QLabel("Randevu Saati")
        self.layout.addWidget(self.label_saat)

        self.saat_secim = QTimeEdit()
        self.saat_secim.setMinimumTime(QTime(9, 0))
        self.saat_secim.setMaximumTime(QTime(16, 0))
        self.layout.addWidget(self.saat_secim)

        self.dersi_al_button = QPushButton("Dersi Al")
        self.dersi_al_button.clicked.connect(self.dersi_al)
        self.layout.addWidget(self.dersi_al_button)

        self.kayitli_derslerim_button = QPushButton("Kayıtlı Derslerim")
        self.kayitli_derslerim_button.clicked.connect(self.kayitli_derslerim_ac)
        self.layout.addWidget(self.kayitli_derslerim_button)

    def get_egitmenler_for_ders(self, ders):
        for kurs in self.kurslar:
            if kurs.adi == ders:
                return [f"{egitmen.isim}, {egitmen.uzmanlik_alani}" for egitmen in kurs.egitmenler]
        return []

    def gun_secildi(self):
        secilen_tarih = self.takvim.selectedDate()
        self.secilen_gun = secilen_tarih.toString(Qt.ISODate)

    def dersi_al(self):
        self.secilen_saat = self.saat_secim.time()
        self.alinan_dersler.append(f"{self.secilen_gun} - {self.secilen_saat.toString()}")
        QMessageBox.information(self, "Bilgi", f"{self.secilen_gun} günü, {self.secilen_saat.toString()} saatine randevu alındı.")

    def kayitli_derslerim_ac(self):
        kayitli_derslerim_penceresi = KayitliDerslerimPenceresi(self.alinan_dersler)
        kayitli_derslerim_penceresi.exec_()

class KayitliDerslerimPenceresi(QDialog):
    def __init__(self, alinan_dersler):
        super().__init__()
        self.setWindowTitle("Alınan Derslerim")
        self.setFixedSize(400, 300)
        self.alinan_dersler = alinan_dersler

        self.layout = QVBoxLayout(self)

        self.label_dersler = QLabel("Alınan Derslerim")
        self.layout.addWidget(self.label_dersler)

        self.liste_alinan_dersler = QListWidget()
        self.liste_alinan_dersler.addItems(self.alinan_dersler)
        self.layout.addWidget(self.liste_alinan_dersler)

        self.sil_button = QPushButton("Sil")
        self.sil_button.clicked.connect(self.ders_sil)
        self.layout.addWidget(self.sil_button)

        self.iptal_button = QPushButton("İptal")
        self.iptal_button.clicked.connect(self.iptal)
        self.layout.addWidget(self.iptal_button)

    def ders_sil(self):
        secilen_dersler = self.liste_alinan_dersler.selectedItems()
        if secilen_dersler:
            secilen_ders = secilen_dersler[0].text()
            self.alinan_dersler.remove(secilen_ders)
            self.liste_alinan_dersler.clear()
            self.liste_alinan_dersler.addItems(self.alinan_dersler)

    def iptal(self):
        self.close()

class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Online Eğitim Platformu")
        self.setFixedSize(800, 600)

        self.kayit_verileri = {}  # Öğrenci verilerini depolamak için bir sözlük
        self.ogretmen_verileri = {}  # Öğretmen verilerini depolamak için bir sözlük

        self.kurslar = [
            Kurs("Matematik", [], "Matematik dersi içeriği"),
            Kurs("Fizik", [], "Fizik dersi içeriği"),
            Kurs("Kimya", [], "Kimya dersi içeriği"),
            Kurs("Biyoloji", [], "Biyoloji dersi içeriği"),
            Kurs("Tarih", [], "Tarih dersi içeriği")
        ]

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("MATS'e Hoş Geldiniz")
        self.label.setAlignment(Qt.AlignCenter)  # Metni ortala
        self.layout.addWidget(self.label)

        self.giris_button = QPushButton("Giriş Yap")
        self.giris_button.clicked.connect(self.giris_yap)
        self.layout.addWidget(self.giris_button)

        self.kayit_button = QPushButton("Kayıt Ol")
        self.kayit_button.clicked.connect(self.kayit_ol)
        self.layout.addWidget(self.kayit_button)

        self.ogretmen_kayit_button = QPushButton("Öğretmen Kayıt")
        self.ogretmen_kayit_button.clicked.connect(self.ogretmen_kayit)
        self.layout.addWidget(self.ogretmen_kayit_button)

    def giris_yap(self):
        giris_penceresi = GirisPenceresi(self.kayit_verileri)
        if giris_penceresi.exec_() == QDialog.Accepted:
            ogrenci = giris_penceresi.get_ogrenci()
            dersler_penceresi = DerslerPenceresi(ogrenci, self.kurslar)
            dersler_penceresi.exec_()

    def kayit_ol(self):
        kayit_penceresi = KayitPenceresi(self.kayit_verileri)
        kayit_penceresi.exec_()

    def ogretmen_kayit(self):
        ogretmen_kayit_penceresi = OgretmenKayitPenceresi(self.ogretmen_verileri, self.kurslar)
        ogretmen_kayit_penceresi.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec_())
