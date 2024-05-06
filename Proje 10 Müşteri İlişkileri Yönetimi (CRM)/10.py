import sys
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QToolButton, QTextEdit, QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QToolButton, QTextEdit, QMessageBox, QTableWidget, QTableWidgetItem


def connect_database():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, isim TEXT, soyisim TEXT, tc_no TEXT UNIQUE, sifre TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS destek_mesajlari (id INTEGER PRIMARY KEY, konu TEXT, mesaj TEXT)")
    connection.commit()
    return connection, cursor



class SaticiGirisSayfasi(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Satıcı Girişi')
        self.setFixedSize(800, 650)  # Pencere boyutu ayarı

        # Başlık etiketi
        self.baslik = QLabel("Satıcı Girişi", self)
        self.baslik.setAlignment(Qt.AlignCenter)

        # Mesajları görüntülemek için tablo oluştur
        self.mesaj_tablosu = QTableWidget()
        self.mesaj_tablosu.setColumnCount(3)
        self.mesaj_tablosu.setHorizontalHeaderLabels(["ID", "Konu", "Mesaj"])
        self.mesaj_tablosu.horizontalHeader().setStretchLastSection(True)

        # Veritabanından mesajları yükle
        self.mesajlari_yukle()

        # Ana düzen
        layout = QVBoxLayout()
        layout.addWidget(self.baslik)
        layout.addWidget(self.mesaj_tablosu)
        self.setLayout(layout)

    def mesajlari_yukle(self):
        # Veritabanı bağlantısını oluştur
        connection, cursor = connect_database()

        # Mesajları veritabanından al ve tabloya ekle
        cursor.execute("SELECT * FROM destek_mesajlari")
        mesajlar = cursor.fetchall()
        self.mesaj_tablosu.setRowCount(len(mesajlar))
        for i, mesaj in enumerate(mesajlar):
            for j, value in enumerate(mesaj):
                item = QTableWidgetItem(str(value))
                self.mesaj_tablosu.setItem(i, j, item)

class MusteriKayitSayfasi(QWidget):
    def __init__(self, ana_pencere):
        super().__init__()
        self.ana_pencere = ana_pencere
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Müşteri Kayıt')
        self.setFixedSize(800, 650)  # Pencere boyutu ayarı

        # İsim etiketi ve giriş kutusu
        self.isim_label = QLabel("İsim:", self)
        self.isim_entry = QLineEdit(self)

        # Soyisim etiketi ve giriş kutusu
        self.soyisim_label = QLabel("Soyisim:", self)
        self.soyisim_entry = QLineEdit(self)

        # TC No etiketi ve giriş kutusu
        self.tc_label = QLabel("TC No:", self)
        self.tc_entry = QLineEdit(self)

        # Şifre etiketi ve giriş kutusu
        self.sifre_label = QLabel("Şifre:", self)
        self.sifre_entry = QLineEdit(self)
        self.sifre_entry.setEchoMode(QLineEdit.Password)

        # Kaydol düğmesi
        self.kaydol_btn = QPushButton("Kaydol", self)
        self.kaydol_btn.clicked.connect(self.kaydol)

        # Geri dön düğmesi
        self.geri_don_btn = QPushButton("Geri Dön", self)
        self.geri_don_btn.clicked.connect(self.geri_don)

        # Ana düzen
        layout = QVBoxLayout()
        layout.addWidget(self.isim_label)
        layout.addWidget(self.isim_entry)
        layout.addWidget(self.soyisim_label)
        layout.addWidget(self.soyisim_entry)
        layout.addWidget(self.tc_label)
        layout.addWidget(self.tc_entry)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre_entry)
        layout.addWidget(self.kaydol_btn)
        layout.addWidget(self.geri_don_btn)  # Geri dön düğmesini layout'a ekle
        self.setLayout(layout)

    def kaydol(self):
        isim = self.isim_entry.text()
        soyisim = self.soyisim_entry.text()
        tc_no = self.tc_entry.text()
        sifre = self.sifre_entry.text()

        # TC no'nun 11 haneli ve sadece sayılardan oluştuğunu kontrol et
        if len(tc_no) != 11 or not tc_no.isdigit():
            QMessageBox.warning(self, "Hata", "TC No 11 haneli olmalı ve sadece sayılardan oluşmalıdır.")
            return

        # Veritabanı bağlantısını oluştur
        connection, cursor = connect_database()

        try:
            # Kullanıcıyı veritabanına ekle
            cursor.execute("INSERT INTO users (isim, soyisim, tc_no, sifre) VALUES (?, ?, ?, ?)",
                           (isim, soyisim, tc_no, sifre))
            connection.commit()
            QMessageBox.information(self, "Başarılı", "Kayıt başarıyla oluşturuldu.")
            self.geri_don()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Hata", "Bu TC No zaten kayıtlıdır. Lütfen farklı bir TC No girin.")

    def geri_don(self):
        # Ana pencereye geri dönme işlemi
        self.ana_pencere.show()
        self.close()


class MusteriGirisSayfasi(QWidget):
    def __init__(self, ana_pencere):
        super().__init__()
        self.ana_pencere = ana_pencere
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Müşteri Girişi')
        self.setFixedSize(800, 650)  # Pencere boyutu ayarı

        # Başlık etiketi
        self.baslik = QLabel("Müşteri Girişi", self)
        self.baslik.setAlignment(Qt.AlignCenter)

        # İsim etiketi ve giriş kutusu
        self.isim_label = QLabel("İsim:", self)
        self.isim_entry = QLineEdit(self)

        # Soyisim etiketi ve giriş kutusu
        self.soyisim_label = QLabel("Soyisim:", self)
        self.soyisim_entry = QLineEdit(self)

        # TC No etiketi ve giriş kutusu
        self.tc_label = QLabel("TC No:", self)
        self.tc_entry = QLineEdit(self)

        # Şifre etiketi ve giriş kutusu
        self.sifre_label = QLabel("Şifre:", self)
        self.sifre_entry = QLineEdit(self)
        self.sifre_entry.setEchoMode(QLineEdit.Password)

        # Giriş düğmesi
        self.giris_btn = QPushButton("Giriş Yap", self)
        self.giris_btn.clicked.connect(self.giris_yap)

        # Kaydol düğmesi
        self.kaydol_btn = QPushButton("Kaydol", self)
        self.kaydol_btn.clicked.connect(self.kaydol)

        # Geri dön butonu
        self.geri_don_btn = QPushButton("Geri Dön", self)
        self.geri_don_btn.clicked.connect(self.geri_don)

        # Ana düzen
        layout = QVBoxLayout()
        layout.addWidget(self.baslik)
        layout.addWidget(self.isim_label)
        layout.addWidget(self.isim_entry)
        layout.addWidget(self.soyisim_label)
        layout.addWidget(self.soyisim_entry)
        layout.addWidget(self.tc_label)
        layout.addWidget(self.tc_entry)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre_entry)
        layout.addWidget(self.giris_btn)
        layout.addWidget(self.kaydol_btn)
        layout.addWidget(self.geri_don_btn)
        self.setLayout(layout)

    def giris_yap(self):
        isim = self.isim_entry.text()
        soyisim = self.soyisim_entry.text()
        tc_no = self.tc_entry.text()
        sifre = self.sifre_entry.text()

        # Veritabanı bağlantısını oluştur
        connection, cursor = connect_database()

        # Kullanıcıyı veritabanında kontrol et
        cursor.execute("SELECT * FROM users WHERE tc_no = ? AND sifre = ?", (tc_no, sifre))
        user = cursor.fetchone()

        if user:
            QMessageBox.information(self, "Giriş Başarılı", "Giriş başarıyla yapıldı.")
            self.destek_sayfasi = DestekSayfasi()
            self.destek_sayfasi.show()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz TC No veya şifre. Lütfen tekrar deneyin.")

    def kaydol(self):
        self.musteri_kayit_sayfasi = MusteriKayitSayfasi(self)  # Müşteri kayıt sayfasını oluştur
        self.musteri_kayit_sayfasi.show()  # Müşteri kayıt sayfasını göster
        self.close()  # Müşteri giriş sayfasını kapat

    def geri_don(self):
        # Ana pencereye geri dönme işlemi
        self.ana_pencere.show()
        self.close()


class DestekSayfasi(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Destek Sayfası')
        self.setFixedSize(800, 650)  # Pencere boyutu ayarı

        # Başlık etiketi
        self.baslik = QLabel("Destek Sayfası", self)
        self.baslik.setAlignment(Qt.AlignCenter)

        # Konu girişi etiketi ve giriş kutusu
        self.konu_label = QLabel("Konu:", self)
        self.konu_entry = QLineEdit(self)

        # Mesaj girişi etiketi ve giriş kutusu
        self.mesaj_label = QLabel("Mesajınız:", self)
        self.mesaj_entry = QTextEdit(self)

        # Gönder düğmesi
        self.gonder_btn = QPushButton("Gönder", self)
        self.gonder_btn.clicked.connect(self.gonder)

        # Geri dön butonu
        self.geri_don_btn = QPushButton("Geri Dön", self)
        self.geri_don_btn.clicked.connect(self.geri_don)

        # Ana düzen
        layout = QVBoxLayout()
        layout.addWidget(self.baslik)
        layout.addWidget(self.konu_label)
        layout.addWidget(self.konu_entry)
        layout.addWidget(self.mesaj_label)
        layout.addWidget(self.mesaj_entry)
        layout.addWidget(self.gonder_btn)
        layout.addWidget(self.geri_don_btn)
        self.setLayout(layout)

    def gonder(self):
        konu = self.konu_entry.text()
        mesaj = self.mesaj_entry.toPlainText()

        # Veritabanı bağlantısını oluştur
        connection, cursor = connect_database()

        try:
            # Mesajı veritabanına ekle
            cursor.execute("INSERT INTO destek_mesajlari (konu, mesaj) VALUES (?, ?)", (konu, mesaj))
            connection.commit()
            QMessageBox.information(self, "Mesajınız Gönderildi", "Mesajınız başarıyla gönderildi.")
            self.geri_don()
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Mesaj gönderilirken bir hata oluştu: {str(e)}")

    def geri_don(self):
        # Müşteri giriş sayfasına geri dönme işlemi
        self.musteri_giris_sayfasi = MusteriGirisSayfasi(self.parent())
        self.musteri_giris_sayfasi.show()
        self.close()


class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ALYU Müşteri Hizmetleri')
        self.setFixedSize(800, 650)  # Pencere boyutu ayarı

        # Başlık etiketi
        self.baslik = QLabel("ALYU MÜŞTERİ HİZMETLERİNE HOŞ GELDİNİZ", self)
        self.baslik.setAlignment(Qt.AlignCenter)

        # Satıcı girişi düğmesi
        self.satici_btn = QToolButton(self)
        self.satici_btn.setText('Satıcı Girişi')
        self.satici_btn.setStyleSheet("QToolButton { background-color: #4CAF50; color: white; border-radius: 5px; }")
        self.satici_btn.setFixedSize(300, 100)  # Düğme boyutu ayarı
        self.satici_btn.clicked.connect(self.satici_giris)

        # Müşteri girişi düğmesi
        self.musteri_btn = QToolButton(self)
        self.musteri_btn.setText('Müşteri Girişi')
        self.musteri_btn.setStyleSheet("QToolButton { background-color: #2196F3; color: white; border-radius: 5px; }")
        self.musteri_btn.setFixedSize(300, 100)  # Düğme boyutu ayarı
        self.musteri_btn.clicked.connect(self.musteri_giris)

        # Butonları yan yana yerleştirmek için yatay düzen
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.satici_btn)
        button_layout.addWidget(self.musteri_btn)

        # Ana düzen
        layout = QVBoxLayout()
        layout.addWidget(self.baslik)
        layout.addStretch(1)  # Başlık etiketinin altına biraz boşluk bırakır
        layout.addLayout(button_layout)  # Yatay düzeni ana düzene ekler
        layout.addStretch(1)  # Düğmelerin altına biraz boşluk bırakır
        self.setLayout(layout)

        # MusteriGirisSayfasi nesnesini oluştur ve sakla
        self.musteri_giris_sayfasi = MusteriGirisSayfasi(self)

    def satici_giris(self):
        self.satici_sayfasi = SaticiGirisSayfasi()
        self.satici_sayfasi.show()

    def musteri_giris(self):
        self.hide()  # Ana pencereyi gizle
        self.musteri_giris_sayfasi.show()  # Saklanan Müşteri Girişi penceresini göster


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec_())
