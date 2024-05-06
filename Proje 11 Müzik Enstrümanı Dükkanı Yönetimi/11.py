import sys
import sqlite3
import random
import string
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QTextEdit

class StokGuncelle(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stok Güncelle")
        self.setGeometry(100, 100, 800, 650)
        self.init_ui()

    def init_ui(self):
        self.label_enstruman = QLabel("Enstrüman Adı:", self)
        self.input_enstruman = QLineEdit(self)
        self.label_stok_adedi = QLabel("Stok Adedi:", self)
        self.input_stok_adedi = QLineEdit(self)
        self.label_fiyat = QLabel("Fiyat:", self)
        self.input_fiyat = QLineEdit(self)
        btn_kaydet = QPushButton("Kaydet", self)
        btn_kaydet.clicked.connect(self.stok_guncelle)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        layout = QVBoxLayout()
        layout.addWidget(self.label_enstruman)
        layout.addWidget(self.input_enstruman)
        layout.addWidget(self.label_stok_adedi)
        layout.addWidget(self.input_stok_adedi)
        layout.addWidget(self.label_fiyat)
        layout.addWidget(self.input_fiyat)
        layout.addWidget(btn_kaydet)
        layout.addWidget(self.tableWidget)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)
        self.setLayout(layout)
        self.tabloyu_doldur()

    def stok_guncelle(self):
        conn = sqlite3.connect('stok_veritabani.db')
        cursor = conn.cursor()
        enstruman_adı = self.input_enstruman.text()
        stok_adedi = self.input_stok_adedi.text()
        fiyat = self.input_fiyat.text()
        cursor.execute("INSERT INTO stok (enstruman_adı, stok_adedi, fiyat) VALUES (?, ?, ?)", (enstruman_adı, stok_adedi, fiyat))
        conn.commit()
        self.tabloyu_doldur()
        conn.close()
        QMessageBox.information(self, "Stok Güncelleme", f"Stok güncellendi:\nEnstrüman Adı: {enstruman_adı}\nStok Adedi: {stok_adedi}\nFiyat: {fiyat}")

    def tabloyu_doldur(self):
        conn = sqlite3.connect('stok_veritabani.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stok")
        rows = cursor.fetchall()
        conn.close()
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(rows):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

class AnaArayuz(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 650)
        self.setWindowTitle("ALYU Enstrümana Hoş Geldiniz")
        label_hosgeldiniz = QLabel("ALYU Enstrümana Hoş Geldiniz", self)
        label_hosgeldiniz.setAlignment(Qt.AlignCenter)
        label_hosgeldiniz.setStyleSheet("font-size: 42px; color: #333; font-weight: bold;")
        btn_musteri = QPushButton("Müşteri Girişi", self)
        btn_musteri.setStyleSheet("background-color: #007bff; color: white; font-weight: bold; border-radius: 10px;")
        btn_musteri.setFixedHeight(40)
        btn_musteri.clicked.connect(self.musteri_girisi_ac)
        btn_satici = QPushButton("Satıcı Girişi", self)
        btn_satici.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; border-radius: 10px;")
        btn_satici.setFixedHeight(40)
        btn_satici.clicked.connect(self.satici_girisi_ac)
        layout = QVBoxLayout()
        layout.addWidget(label_hosgeldiniz)
        layout.addWidget(btn_musteri)
        layout.addWidget(btn_satici)
        self.setLayout(layout)
        self.show()

    def musteri_girisi_ac(self):
        self.musteri_girisi_pencere = MusteriGirisi()
        self.musteri_girisi_pencere.show()

    def satici_girisi_ac(self):
        self.satici_girisi_pencere = SaticiGirisi()
        self.satici_girisi_pencere.show()

class MusteriGirisi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Müşteri Girişi")
        self.setGeometry(100, 100, 800, 650)
        self.init_ui()
        self.satinalinanlar_listesi = []

    def init_ui(self):
        btn_destek = QPushButton("Destek", self)
        btn_destek.setStyleSheet("background-color: #008CBA; color: white; font-weight: bold;")
        btn_destek.clicked.connect(self.destek_sayfasi_ac)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Ürün", "Adet", "Fiyat"])
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget.setSelectionMode(QTableWidget.SingleSelection)
        btn_satinal = QPushButton("Satın Al", self)
        btn_satinal.clicked.connect(self.satinal)
        btn_satinalinanlar = QPushButton("Satın Alınanlar", self)
        btn_satinalinanlar.clicked.connect(self.satinalinanlar_goster)
        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_destek)
        button_layout.addWidget(btn_satinal)
        button_layout.addWidget(btn_satinalinanlar)
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)
        self.veritabani_baglan()

    def veritabani_baglan(self):
        db = sqlite3.connect("stok_veritabani.db")
        query = db.cursor()
        query.execute("SELECT * FROM stok")
        row = 0
        while True:
            data = query.fetchone()
            if data is None:
                break
            self.tableWidget.insertRow(row)
            for column in range(3):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(data[column])))
            row += 1
        db.close()

    def destek_sayfasi_ac(self):
        self.destek_sayfasi = DestekSayfasi()
        self.destek_sayfasi.show()

    def satinal(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            adet_item = self.tableWidget.item(selected_row, 1)
            if adet_item is not None:
                current_adet = int(adet_item.text())
                if current_adet > 0:
                    reply = QMessageBox.question(self, "Satın Alma Onayı",
                                                 f"Seçilen üründen bir tane satın almak istediğinize emin misiniz?",
                                                 QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        new_adet = current_adet - 1
                        adet_item.setText(str(new_adet))
                        urun_item = self.tableWidget.item(selected_row, 0)
                        fiyat_item = self.tableWidget.item(selected_row, 2)
                        satis_kodu = self.generate_satis_kodu()
                        self.satinalinanlar_listesi.append((urun_item.text(), fiyat_item.text(), satis_kodu))
                        QMessageBox.information(self, "Satın Alma Başarılı",
                                                f"Satın alma işlemi başarıyla gerçekleştirildi.\nSatış Kodu: {satis_kodu}")
                else:
                    QMessageBox.warning(self, "Stokta Yok", "Üzgünüz, seçilen ürün stokta bulunmamaktadır.")
            else:
                QMessageBox.warning(self, "Hata", "Ürün adet bilgisine ulaşılamadı.")
        else:
            QMessageBox.warning(self, "Satın Alma Hatası", "Lütfen satın almak istediğiniz ürünü tablodan seçin.")

    def generate_satis_kodu(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    def satinalinanlar_goster(self):
        if self.satinalinanlar_listesi:
            satinalinanlar_str = ""
            for urun, fiyat, satis_kodu in self.satinalinanlar_listesi:
                satinalinanlar_str += f"Ürün: {urun}, Fiyat: {fiyat}, Satış Kodu: {satis_kodu}\n"
            QMessageBox.information(self, "Satın Alınanlar", satinalinanlar_str)
        else:
            QMessageBox.information(self, "Satın Alınanlar", "Henüz satın alınan bir ürün bulunmamaktadır.")

class SaticiGirisi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Satıcı Girişi")
        self.setGeometry(100, 100, 800, 650)
        self.init_ui()

    def init_ui(self):
        label_tc = QLabel("TC:", self)
        self.input_tc = QLineEdit(self)
        label_sifre = QLabel("Şifre:", self)
        self.input_sifre = QLineEdit(self)
        self.input_sifre.setEchoMode(QLineEdit.Password)
        btn_kayit_ol = QPushButton("Kayıt Ol", self)
        btn_kayit_ol.clicked.connect(self.kayit_ol)
        btn_giris = QPushButton("Giriş Yap", self)
        btn_giris.clicked.connect(self.giris_kontrol)
        layout = QVBoxLayout()
        layout.addWidget(label_tc)
        layout.addWidget(self.input_tc)
        layout.addWidget(label_sifre)
        layout.addWidget(self.input_sifre)
        layout.addWidget(btn_kayit_ol)
        layout.addWidget(btn_giris)
        self.setLayout(layout)

    def giris_kontrol(self):
        tc = self.input_tc.text()
        sifre = self.input_sifre.text()
        if not tc or not sifre:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen TC ve şifre alanlarını doldurun.")
            return
        if not self.kullanici_kayitli_mi(tc):
            QMessageBox.warning(self, "Kayıt Bulunamadı", "Giriş yapmak için önce kaydolmalısınız.")
            return
        self.stok_guncelle_pencere = StokGuncelle()
        self.stok_guncelle_pencere.show()
        self.close()

    def kullanici_kayitli_mi(self, tc):
        conn = sqlite3.connect('kullanici_veritabani.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kullanicilar WHERE tc = ?", (tc,))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def kayit_ol(self):
        self.kayit_ol_penceresi = KayitOl()
        self.kayit_ol_penceresi.show()

class KayitOl(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kayıt Ol")
        self.setGeometry(100, 100, 300, 200)
        self.init_ui()

    def init_ui(self):
        self.label_tc = QLabel("TC:", self)
        self.input_tc = QLineEdit(self)
        self.label_isim = QLabel("İsim:", self)
        self.input_isim = QLineEdit(self)
        self.label_soyisim = QLabel("Soyisim:", self)
        self.input_soyisim = QLineEdit(self)
        self.label_sifre = QLabel("Şifre:", self)
        self.input_sifre = QLineEdit(self)
        self.input_sifre.setEchoMode(QLineEdit.Password)
        self.btn_kayit = QPushButton("Kayıt Ol", self)
        self.btn_kayit.clicked.connect(self.kayit_ol)
        layout = QVBoxLayout()
        layout.addWidget(self.label_tc)
        layout.addWidget(self.input_tc)
        layout.addWidget(self.label_isim)
        layout.addWidget(self.input_isim)
        layout.addWidget(self.label_soyisim)
        layout.addWidget(self.input_soyisim)
        layout.addWidget(self.label_sifre)
        layout.addWidget(self.input_sifre)
        layout.addWidget(self.btn_kayit)
        self.setLayout(layout)

    def kayit_ol(self):
        tc = self.input_tc.text()
        isim = self.input_isim.text()
        soyisim = self.input_soyisim.text()
        sifre = self.input_sifre.text()
        if not tc or not isim or not soyisim or not sifre:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return
        conn = sqlite3.connect('kullanici_veritabani.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO kullanicilar (tc, isim, soyisim, sifre) VALUES (?, ?, ?, ?)", (tc, isim, soyisim, sifre))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Kayıt Başarılı", "Kayıt işlemi başarıyla tamamlandı.")

class DestekSayfasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Destek")
        self.setGeometry(100, 100, 300, 200)
        self.init_ui()

    def init_ui(self):
        self.label_destek = QLabel("Destek Hattı: 123456789", self)
        self.label_destek.setFont(QFont('Arial', 14))
        layout = QVBoxLayout()
        layout.addWidget(self.label_destek)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ana_arayuz = AnaArayuz()
    sys.exit(app.exec_())
