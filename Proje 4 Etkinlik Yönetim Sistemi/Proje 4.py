import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, \
    QMessageBox, QLineEdit, QVBoxLayout, QHeaderView, QDialog
from PyQt5.QtGui import QFont
import random
from datetime import datetime, timedelta


class KayitOlEkrani(QDialog):
    def __init__(self, ana_pencere, giris_ekrani):
        super().__init__()
        self.setWindowTitle('Kayıt Ol')
        self.setGeometry(400, 200, 300, 250)

        self.giris_ekrani = giris_ekrani

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        self.kullanici_adi_label = QLabel("Kullanıcı Adı:")
        self.kullanici_adi_girdi = QLineEdit()
        layout.addWidget(self.kullanici_adi_label)
        layout.addWidget(self.kullanici_adi_girdi)

        self.sifre_label = QLabel("Şifre:")
        self.sifre_girdi = QLineEdit()
        self.sifre_girdi.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre_girdi)

        self.ad_soyad_label = QLabel("Ad Soyad:")
        self.ad_soyad_girdi = QLineEdit()
        layout.addWidget(self.ad_soyad_label)
        layout.addWidget(self.ad_soyad_girdi)

        self.gmail_label = QLabel("Gmail:")
        self.gmail_girdi = QLineEdit()
        layout.addWidget(self.gmail_label)
        layout.addWidget(self.gmail_girdi)

        self.kayit_ol_buton = QPushButton("Kayıt Ol")
        self.kayit_ol_buton.clicked.connect(self.kayit_ol)
        layout.addWidget(self.kayit_ol_buton)

        self.setLayout(layout)

        self.ana_pencere = ana_pencere

    def kayit_ol(self):
        kullanici_adi = self.kullanici_adi_girdi.text()
        sifre = self.sifre_girdi.text()
        ad_soyad = self.ad_soyad_girdi.text()
        gmail = self.gmail_girdi.text()

        # Kullanıcı adı ve şifre kontrolü
        if kullanici_adi == "" or sifre == "":
            QMessageBox.warning(self, 'Uyarı', 'Kullanıcı adı ve şifre boş olamaz!')
        else:
            # Kayıt işlemi gerçekleştir
            # Bu noktada normalde bir veritabanı işlemi yapılır

            # Kayıt olan kullanıcı bilgilerini giriş ekranına aktar
            self.giris_ekrani.kullanici_bilgisi_ekle(kullanici_adi, sifre)

            QMessageBox.information(self, 'Kayıt Başarılı', 'Kayıt işlemi başarıyla tamamlandı!')

            # Kayıt işlemi tamamlandığında ana pencereyi göster
            self.ana_pencere.show()
            self.close()


class GirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Kullanıcı Girişi ve Kayıt Ol')
        self.setGeometry(400, 200, 300, 250)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        self.kullanici_adi_label = QLabel("Kullanıcı Adı:")
        self.kullanici_adi_girdi = QLineEdit()
        layout.addWidget(self.kullanici_adi_label)
        layout.addWidget(self.kullanici_adi_girdi)

        self.sifre_label = QLabel("Şifre:")
        self.sifre_girdi = QLineEdit()
        self.sifre_girdi.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre_girdi)

        self.giris_buton = QPushButton("Giriş")
        self.giris_buton.clicked.connect(self.giris)
        layout.addWidget(self.giris_buton)

        self.kayit_ol_buton = QPushButton("Kayıt Ol")
        self.kayit_ol_buton.clicked.connect(self.kayit_ol)
        layout.addWidget(self.kayit_ol_buton)

        self.setLayout(layout)

        # Kayıt olan kullanıcı bilgilerini saklamak için bir sözlük oluştur
        self.kullanici_bilgileri = {}

    def giris(self):
        kullanici_adi = self.kullanici_adi_girdi.text()
        sifre = self.sifre_girdi.text()

        # Kullanıcı adı ve şifreyi kontrol et
        if kullanici_adi in self.kullanici_bilgileri and self.kullanici_bilgileri[kullanici_adi] == sifre:
            self.acilis_ekrani = AnaPencere()
            self.acilis_ekrani.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Uyarı', 'Geçersiz kullanıcı adı veya şifre!')

    def kayit_ol(self):
        # Kayıt olma ekranını göster
        self.kayit_ol_ekrani = KayitOlEkrani(self, self)
        self.kayit_ol_ekrani.show()
        self.hide()

    def kullanici_bilgisi_ekle(self, kullanici_adi, sifre):
        # Kayıt olan kullanıcı bilgilerini sakla
        self.kullanici_bilgileri[kullanici_adi] = sifre


class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Etkinlik Yönetim Sistemi')
        self.setGeometry(400, 200, 900, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        self.etkinlik_table = QTableWidget()
        self.etkinlik_table.setColumnCount(4)
        self.etkinlik_table.setHorizontalHeaderLabels(["Etkinlik Adı", "Tarih", "Saat", "Bilet Sayısı"])

        # Arayüz tasarımını düzenle
        self.etkinlik_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Seçim modunu SingleSelection olarak ayarla
        self.etkinlik_table.setSelectionMode(QTableWidget.SingleSelection)

        layout.addWidget(self.etkinlik_table)

        self.bilet_al_buton = QPushButton("Bilet Al")
        self.bilet_al_buton.clicked.connect(self.bilet_al)

        self.satinalinan_biletler_buton = QPushButton("Satın Alınan Biletler")
        self.satinalinan_biletler_buton.clicked.connect(self.satinalinan_biletler)

        layout.addWidget(self.bilet_al_buton)
        layout.addWidget(self.satinalinan_biletler_buton)

        self.etkinlik_olustur()

        self.setLayout(layout)

        self.satinalinan_biletler_listesi = []

    def etkinlik_olustur(self):
        etkinlikler = self.random_etkinlikler_olustur(30)
        self.etkinlik_table.setRowCount(len(etkinlikler))

        for i, (etkinlik_adi, tarih, saat, bilet_sayisi) in enumerate(etkinlikler):
            self.etkinlik_table.setItem(i, 0, QTableWidgetItem(etkinlik_adi))
            self.etkinlik_table.setItem(i, 1, QTableWidgetItem(tarih))
            self.etkinlik_table.setItem(i, 2, QTableWidgetItem(saat))
            self.etkinlik_table.setItem(i, 3, QTableWidgetItem(str(bilet_sayisi)))

    def bilet_al(self):
        secili_satir = self.etkinlik_table.currentRow()
        if secili_satir != -1:
            bilet_sayisi_item = self.etkinlik_table.item(secili_satir, 3)
            bilet_sayisi = int(bilet_sayisi_item.text())
            if bilet_sayisi > 0:
                etkinlik_saat_item = self.etkinlik_table.item(secili_satir, 2)  # Etkinlik saatini al
                etkinlik_saat = etkinlik_saat_item.text()  # Etkinlik saatini metin olarak al
                etkinlik_tarih_item = self.etkinlik_table.item(secili_satir, 1)  # Etkinlik tarihini al
                etkinlik_tarih = etkinlik_tarih_item.text()  # Etkinlik tarihini metin olarak al
                self.etkinlik_table.setItem(secili_satir, 3, QTableWidgetItem(str(bilet_sayisi - 1)))
                self.satinalinan_biletler_listesi.append((self.etkinlik_table.item(secili_satir, 0).text(), etkinlik_tarih, etkinlik_saat))  # Bileti aldığımız tarih ve saat ekleniyor
                QMessageBox.information(self, 'Bilet Alındı', 'Bilet başarıyla satın alındı!')
            else:
                QMessageBox.warning(self, 'Hata', 'Üzgünüz, biletler tükenmiş!')

    def satinalinan_biletler(self):
        dialog = SatinAlinanBiletler(self.satinalinan_biletler_listesi, self)
        dialog.exec_()

    def iade_edilen_bilet(self, bilet_adi):
        for i in range(self.etkinlik_table.rowCount()):
            etkinlik_adi_item = self.etkinlik_table.item(i, 0)
            if etkinlik_adi_item and etkinlik_adi_item.text() == bilet_adi:
                bilet_sayisi_item = self.etkinlik_table.item(i, 3)
                bilet_sayisi = int(bilet_sayisi_item.text())
                self.etkinlik_table.setItem(i, 3, QTableWidgetItem(str(bilet_sayisi + 1)))
                break

    def random_etkinlikler_olustur(self, count):
        etkinlikler = [
            "NY Film Festival",
            "SXSW Music Festival",
            "Coachella Valley Festival",
            "Comic-Con International",
            "New Orleans Jazz Festival",
            "Burning Man",
            "Electric Daisy Carnival",
            "Art Basel Miami",
            "Lollapalooza",
            "Tribeca Film Festival",
            "NY Fashion Week",
            "Ultra Music Festival",
            "SXSW Film Festival",
            "Seattle Int'l Film Festival",
            "Austin City Limits Festival",
            "Chicago Int'l Film Festival",
            "Sundance Film Festival",
            "Bonnaroo Music & Arts",
            "Miami Int'l Film Festival",
            "NY Comedy Festival",
            "Houston Livestock Show",
            "Essence Music Festival",
            "Voodoo Music + Arts",
            "Monterey Jazz Festival",
            "Detroit Jazz Festival",
            "Toronto Int'l Film Festival",
            "NY City Wine & Food Festival",
            "Life is Beautiful Festival",
            "San Diego Comic-Con",
            "Telluride Film Festival",
        ]

        etkinlik_tarihleri = [
            datetime.now() + timedelta(days=random.randint(1, 365)) for _ in range(count)
        ]

        etkinlik_saatleri = [
            datetime.strftime(datetime.now() + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59)),
                              "%H:%M")
            for _ in range(count)
        ]

        bilet_sayilari = [random.randint(50, 200) for _ in range(count)]

        etkinlikler_with_dates = [
            (etkinlik, tarih.strftime("%d/%m/%Y"), saat, bilet_sayisi) for etkinlik, tarih, saat, bilet_sayisi in
            zip(etkinlikler, etkinlik_tarihleri, etkinlik_saatleri, bilet_sayilari)
        ]

        return etkinlikler_with_dates


class SatinAlinanBiletler(QDialog):
    def __init__(self, biletler, ana_pencere):
        super().__init__()
        self.setWindowTitle('Satın Alınan Biletler')
        self.setMinimumWidth(700)
        self.setMinimumHeight(300)

        self.ana_pencere = ana_pencere

        layout = QVBoxLayout()

        self.biletler_list = QTableWidget()
        self.biletler_list.setColumnCount(4)
        self.biletler_list.setHorizontalHeaderLabels(["Bilet Adı", "Tarih", "Saat", "İade Et"])

        layout.addWidget(self.biletler_list)

        self.setLayout(layout)

        self.biletler = biletler

        self.biletler_list.setRowCount(len(biletler))

        for i, bilet in enumerate(biletler):
            bilet_item = QTableWidgetItem(bilet[0])
            self.biletler_list.setItem(i, 0, bilet_item)

            tarih_item = QTableWidgetItem(bilet[1])  # Biletin alındığı tarihi ekle
            self.biletler_list.setItem(i, 1, tarih_item)

            saat_item = QTableWidgetItem(bilet[2])  # Biletin alındığı saati ekle
            self.biletler_list.setItem(i, 2, saat_item)

            iade_button = QPushButton("İade Et")
            iade_button.clicked.connect(lambda checked, row=i: self.iade_et(row))
            self.biletler_list.setCellWidget(i, 3, iade_button)

        # Tablo genişliğini ayarla
        self.biletler_list.setColumnWidth(0, 250)
        self.biletler_list.setColumnWidth(1, 100)
        self.biletler_list.setColumnWidth(2, 100)

    def iade_et(self, row):
        # İade etmek istenen biletin adını al
        bilet_adi = self.biletler_list.item(row, 0).text()

        # İade işlemini gerçekleştir
        self.ana_pencere.iade_edilen_bilet(bilet_adi)
        self.biletler.remove((bilet_adi, self.biletler_list.item(row, 1).text(), self.biletler_list.item(row, 2).text()))  # Satın alınan biletlerden çıkar

        QMessageBox.information(self, 'Bilet İade', f'{bilet_adi} bilet başarıyla iade edildi!')

        # Satırı kaldır
        self.biletler_list.removeRow(row)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Yeni bir tema deneyelim (siyah-beyaz tonlar)
    app.setStyleSheet("""
        QWidget {
            background-color: #ffffff;
            color: #000000;
        }
        QPushButton {
            background-color: #000000;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #333333;
        }
        QTableWidget {
            background-color: #ffffff;
            border: 1px solid #000000;
            border-radius: 4px;
        }
        QHeaderView::section {
            background-color: #000000;
            color: #ffffff;
            padding: 4px 8px;
        }
        QLabel {
            color: #000000;
        }
        QLineEdit {
            border: 1px solid #000000;
            border-radius: 4px;
            padding: 4px 8px;
        }
        QMessageBox {
            background-color: #ffffff;
        }
    """)
    giris_ekrani = GirisEkrani()
    giris_ekrani.show()
    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, \
    QMessageBox, QLineEdit, QVBoxLayout, QHeaderView, QDialog
from PyQt5.QtGui import QFont
import random
from datetime import datetime, timedelta


class KayitOlEkrani(QDialog):
    def __init__(self, ana_pencere, giris_ekrani):
        super().__init__()
        self.setWindowTitle('Kayıt Ol')
        self.setGeometry(400, 200, 300, 250)

        self.giris_ekrani = giris_ekrani

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        self.kullanici_adi_label = QLabel("Kullanıcı Adı:")
        self.kullanici_adi_girdi = QLineEdit()
        layout.addWidget(self.kullanici_adi_label)
        layout.addWidget(self.kullanici_adi_girdi)

        self.sifre_label = QLabel("Şifre:")
        self.sifre_girdi = QLineEdit()
        self.sifre_girdi.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre_girdi)

        self.ad_soyad_label = QLabel("Ad Soyad:")
        self.ad_soyad_girdi = QLineEdit()
        layout.addWidget(self.ad_soyad_label)
        layout.addWidget(self.ad_soyad_girdi)

        self.gmail_label = QLabel("Gmail:")
        self.gmail_girdi = QLineEdit()
        layout.addWidget(self.gmail_label)
        layout.addWidget(self.gmail_girdi)

        self.kayit_ol_buton = QPushButton("Kayıt Ol")
        self.kayit_ol_buton.clicked.connect(self.kayit_ol)
        layout.addWidget(self.kayit_ol_buton)

        self.setLayout(layout)

        self.ana_pencere = ana_pencere

    def kayit_ol(self):
        kullanici_adi = self.kullanici_adi_girdi.text()
        sifre = self.sifre_girdi.text()
        ad_soyad = self.ad_soyad_girdi.text()
        gmail = self.gmail_girdi.text()

        # Kullanıcı adı ve şifre kontrolü
        if kullanici_adi == "" or sifre == "":
            QMessageBox.warning(self, 'Uyarı', 'Kullanıcı adı ve şifre boş olamaz!')
        else:
            # Kayıt işlemi gerçekleştir
            # Bu noktada normalde bir veritabanı işlemi yapılır

            # Kayıt olan kullanıcı bilgilerini giriş ekranına aktar
            self.giris_ekrani.kullanici_bilgisi_ekle(kullanici_adi, sifre)

            QMessageBox.information(self, 'Kayıt Başarılı', 'Kayıt işlemi başarıyla tamamlandı!')

            # Kayıt işlemi tamamlandığında ana pencereyi göster
            self.ana_pencere.show()
            self.close()


class GirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Kullanıcı Girişi ve Kayıt Ol')
        self.setGeometry(400, 200, 300, 250)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        self.kullanici_adi_label = QLabel("Kullanıcı Adı:")
        self.kullanici_adi_girdi = QLineEdit()
        layout.addWidget(self.kullanici_adi_label)
        layout.addWidget(self.kullanici_adi_girdi)

        self.sifre_label = QLabel("Şifre:")
        self.sifre_girdi = QLineEdit()
        self.sifre_girdi.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre_girdi)

        self.giris_buton = QPushButton("Giriş")
        self.giris_buton.clicked.connect(self.giris)
        layout.addWidget(self.giris_buton)

        self.kayit_ol_buton = QPushButton("Kayıt Ol")
        self.kayit_ol_buton.clicked.connect(self.kayit_ol)
        layout.addWidget(self.kayit_ol_buton)

        self.setLayout(layout)

        # Kayıt olan kullanıcı bilgilerini saklamak için bir sözlük oluştur
        self.kullanici_bilgileri = {}

    def giris(self):
        kullanici_adi = self.kullanici_adi_girdi.text()
        sifre = self.sifre_girdi.text()

        # Kullanıcı adı ve şifreyi kontrol et
        if kullanici_adi in self.kullanici_bilgileri and self.kullanici_bilgileri[kullanici_adi] == sifre:
            self.acilis_ekrani = AnaPencere()
            self.acilis_ekrani.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Uyarı', 'Geçersiz kullanıcı adı veya şifre!')

    def kayit_ol(self):
        # Kayıt olma ekranını göster
        self.kayit_ol_ekrani = KayitOlEkrani(self, self)
        self.kayit_ol_ekrani.show()
        self.hide()

    def kullanici_bilgisi_ekle(self, kullanici_adi, sifre):
        # Kayıt olan kullanıcı bilgilerini sakla
        self.kullanici_bilgileri[kullanici_adi] = sifre


class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Etkinlik Yönetim Sistemi')
        self.setGeometry(400, 200, 900, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        self.etkinlik_table = QTableWidget()
        self.etkinlik_table.setColumnCount(4)
        self.etkinlik_table.setHorizontalHeaderLabels(["Etkinlik Adı", "Tarih", "Saat", "Bilet Sayısı"])

        # Arayüz tasarımını düzenle
        self.etkinlik_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Seçim modunu SingleSelection olarak ayarla
        self.etkinlik_table.setSelectionMode(QTableWidget.SingleSelection)

        layout.addWidget(self.etkinlik_table)

        self.bilet_al_buton = QPushButton("Bilet Al")
        self.bilet_al_buton.clicked.connect(self.bilet_al)

        self.satinalinan_biletler_buton = QPushButton("Satın Alınan Biletler")
        self.satinalinan_biletler_buton.clicked.connect(self.satinalinan_biletler)

        layout.addWidget(self.bilet_al_buton)
        layout.addWidget(self.satinalinan_biletler_buton)

        self.etkinlik_olustur()

        self.setLayout(layout)

        self.satinalinan_biletler_listesi = []

    def etkinlik_olustur(self):
        etkinlikler = self.random_etkinlikler_olustur(30)
        self.etkinlik_table.setRowCount(len(etkinlikler))

        for i, (etkinlik_adi, tarih, saat, bilet_sayisi) in enumerate(etkinlikler):
            self.etkinlik_table.setItem(i, 0, QTableWidgetItem(etkinlik_adi))
            self.etkinlik_table.setItem(i, 1, QTableWidgetItem(tarih))
            self.etkinlik_table.setItem(i, 2, QTableWidgetItem(saat))
            self.etkinlik_table.setItem(i, 3, QTableWidgetItem(str(bilet_sayisi)))

    def bilet_al(self):
        secili_satir = self.etkinlik_table.currentRow()
        if secili_satir != -1:
            bilet_sayisi_item = self.etkinlik_table.item(secili_satir, 3)
            bilet_sayisi = int(bilet_sayisi_item.text())
            if bilet_sayisi > 0:
                etkinlik_saat_item = self.etkinlik_table.item(secili_satir, 2)  # Etkinlik saatini al
                etkinlik_saat = etkinlik_saat_item.text()  # Etkinlik saatini metin olarak al
                etkinlik_tarih_item = self.etkinlik_table.item(secili_satir, 1)  # Etkinlik tarihini al
                etkinlik_tarih = etkinlik_tarih_item.text()  # Etkinlik tarihini metin olarak al
                self.etkinlik_table.setItem(secili_satir, 3, QTableWidgetItem(str(bilet_sayisi - 1)))
                self.satinalinan_biletler_listesi.append((self.etkinlik_table.item(secili_satir, 0).text(), etkinlik_tarih, etkinlik_saat))  # Bileti aldığımız tarih ve saat ekleniyor
                QMessageBox.information(self, 'Bilet Alındı', 'Bilet başarıyla satın alındı!')
            else:
                QMessageBox.warning(self, 'Hata', 'Üzgünüz, biletler tükenmiş!')

    def satinalinan_biletler(self):
        dialog = SatinAlinanBiletler(self.satinalinan_biletler_listesi, self)
        dialog.exec_()

    def iade_edilen_bilet(self, bilet_adi):
        for i in range(self.etkinlik_table.rowCount()):
            etkinlik_adi_item = self.etkinlik_table.item(i, 0)
            if etkinlik_adi_item and etkinlik_adi_item.text() == bilet_adi:
                bilet_sayisi_item = self.etkinlik_table.item(i, 3)
                bilet_sayisi = int(bilet_sayisi_item.text())
                self.etkinlik_table.setItem(i, 3, QTableWidgetItem(str(bilet_sayisi + 1)))
                break

    def random_etkinlikler_olustur(self, count):
        etkinlikler = [
            "NY Film Festival",
            "SXSW Music Festival",
            "Coachella Valley Festival",
            "Comic-Con International",
            "New Orleans Jazz Festival",
            "Burning Man",
            "Electric Daisy Carnival",
            "Art Basel Miami",
            "Lollapalooza",
            "Tribeca Film Festival",
            "NY Fashion Week",
            "Ultra Music Festival",
            "SXSW Film Festival",
            "Seattle Int'l Film Festival",
            "Austin City Limits Festival",
            "Chicago Int'l Film Festival",
            "Sundance Film Festival",
            "Bonnaroo Music & Arts",
            "Miami Int'l Film Festival",
            "NY Comedy Festival",
            "Houston Livestock Show",
            "Essence Music Festival",
            "Voodoo Music + Arts",
            "Monterey Jazz Festival",
            "Detroit Jazz Festival",
            "Toronto Int'l Film Festival",
            "NY City Wine & Food Festival",
            "Life is Beautiful Festival",
            "San Diego Comic-Con",
            "Telluride Film Festival",
        ]

        etkinlik_tarihleri = [
            datetime.now() + timedelta(days=random.randint(1, 365)) for _ in range(count)
        ]

        etkinlik_saatleri = [
            datetime.strftime(datetime.now() + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59)),
                              "%H:%M")
            for _ in range(count)
        ]

        bilet_sayilari = [random.randint(50, 200) for _ in range(count)]

        etkinlikler_with_dates = [
            (etkinlik, tarih.strftime("%d/%m/%Y"), saat, bilet_sayisi) for etkinlik, tarih, saat, bilet_sayisi in
            zip(etkinlikler, etkinlik_tarihleri, etkinlik_saatleri, bilet_sayilari)
        ]

        return etkinlikler_with_dates


class SatinAlinanBiletler(QDialog):
    def __init__(self, biletler, ana_pencere):
        super().__init__()
        self.setWindowTitle('Satın Alınan Biletler')
        self.setMinimumWidth(700)
        self.setMinimumHeight(300)

        self.ana_pencere = ana_pencere

        layout = QVBoxLayout()

        self.biletler_list = QTableWidget()
        self.biletler_list.setColumnCount(4)
        self.biletler_list.setHorizontalHeaderLabels(["Bilet Adı", "Tarih", "Saat", "İade Et"])

        layout.addWidget(self.biletler_list)

        self.setLayout(layout)

        self.biletler = biletler

        self.biletler_list.setRowCount(len(biletler))

        for i, bilet in enumerate(biletler):
            bilet_item = QTableWidgetItem(bilet[0])
            self.biletler_list.setItem(i, 0, bilet_item)

            tarih_item = QTableWidgetItem(bilet[1])  # Biletin alındığı tarihi ekle
            self.biletler_list.setItem(i, 1, tarih_item)

            saat_item = QTableWidgetItem(bilet[2])  # Biletin alındığı saati ekle
            self.biletler_list.setItem(i, 2, saat_item)

            iade_button = QPushButton("İade Et")
            iade_button.clicked.connect(lambda checked, row=i: self.iade_et(row))
            self.biletler_list.setCellWidget(i, 3, iade_button)

        # Tablo genişliğini ayarla
        self.biletler_list.setColumnWidth(0, 250)
        self.biletler_list.setColumnWidth(1, 100)
        self.biletler_list.setColumnWidth(2, 100)

    def iade_et(self, row):
        # İade etmek istenen biletin adını al
        bilet_adi = self.biletler_list.item(row, 0).text()

        # İade işlemini gerçekleştir
        self.ana_pencere.iade_edilen_bilet(bilet_adi)
        self.biletler.remove((bilet_adi, self.biletler_list.item(row, 1).text(), self.biletler_list.item(row, 2).text()))  # Satın alınan biletlerden çıkar

        QMessageBox.information(self, 'Bilet İade', f'{bilet_adi} bilet başarıyla iade edildi!')

        # Satırı kaldır
        self.biletler_list.removeRow(row)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Yeni bir tema deneyelim (siyah-beyaz tonlar)
    app.setStyleSheet("""
        QWidget {
            background-color: #ffffff;
            color: #000000;
        }
        QPushButton {
            background-color: #000000;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #333333;
        }
        QTableWidget {
            background-color: #ffffff;
            border: 1px solid #000000;
            border-radius: 4px;
        }
        QHeaderView::section {
            background-color: #000000;
            color: #ffffff;
            padding: 4px 8px;
        }
        QLabel {
            color: #000000;
        }
        QLineEdit {
            border: 1px solid #000000;
            border-radius: 4px;
            padding: 4px 8px;
        }
        QMessageBox {
            background-color: #ffffff;
        }
    """)
    giris_ekrani = GirisEkrani()
    giris_ekrani.show()
    sys.exit(app.exec_())
