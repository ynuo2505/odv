from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QComboBox, QSpinBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QIntValidator

class Kullanici:
    def __init__(self, kullanici_adi, sifre, ad, yas, cinsiyet):
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre
        self.ad = ad
        self.yas = yas
        self.cinsiyet = cinsiyet
        self.saglik_kaydi = []
        self.egzersizler = []

    def kayit_ekle(self, kayit):
        self.saglik_kaydi.append(kayit)

    def egzersiz_ekle(self, egzersiz):
        self.egzersizler.append(egzersiz)

    def rapor_olustur(self):
        return self.ad, self.yas, self.saglik_kaydi, self.egzersizler

class AnaEkran(QWidget):
    def __init__(self, kullanici):
        super().__init__()

        self.kullanici = kullanici
        self.rapor_window = None  

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Fitness Sayfası - {}'.format(self.kullanici.kullanici_adi))
        self.setGeometry(200, 200, 800, 400)  

        layout = QVBoxLayout()

        self.bilgi_label = QLabel('Hoş geldiniz, {}!'.format(self.kullanici.ad))
        layout.addWidget(self.bilgi_label)

        self.saglik_kaydi_tablosu = QTableWidget()
        self.saglik_kaydi_tablosu.setColumnCount(2)  
        self.saglik_kaydi_tablosu.setHorizontalHeaderLabels(["Boy (cm)", "Kilo (kg)"])
        self.saglik_kaydi_tablosu.setStyleSheet("background-color: lightgray; color: black;")  
        layout.addWidget(self.saglik_kaydi_tablosu)

        self.egzersiz_tablosu = QTableWidget()
        self.egzersiz_tablosu.setColumnCount(3)  
        self.egzersiz_tablosu.setHorizontalHeaderLabels(["Egzersiz Adı", "Süre (dk)", "Tekrar Sayısı"])
        self.egzersiz_tablosu.setStyleSheet("background-color: lightgray; color: black;")  
        layout.addWidget(self.egzersiz_tablosu)

        self.saglik_kaydi_button = QPushButton('Sağlık Verileri')
        self.saglik_kaydi_button.clicked.connect(self.saglik_kaydi_ekle)
        layout.addWidget(self.saglik_kaydi_button)

        self.egzersiz_ekle_button = QPushButton('Egzersiz Ekle')
        self.egzersiz_ekle_button.clicked.connect(self.egzersiz_ekle)
        layout.addWidget(self.egzersiz_ekle_button)

        self.rapor_olustur_button = QPushButton('Rapor Oluştur')
        self.rapor_olustur_button.clicked.connect(self.rapor_olustur)
        layout.addWidget(self.rapor_olustur_button)

        self.setLayout(layout)

    def saglik_kaydi_ekle(self):
        self.saglik_kaydi_penceresi = SaglikKaydiPenceresi(self.kullanici)
        self.saglik_kaydi_penceresi.saglik_kaydi_signal.connect(self.guncelle_boy_kilo_tablosu)
        self.saglik_kaydi_penceresi.setStyleSheet("background-color: rgb(40, 44, 52); color: white;")
        self.saglik_kaydi_penceresi.show()

    def egzersiz_ekle(self):
        self.egzersiz_ekle_penceresi = EgzersizEklePenceresi(self.kullanici)
        self.egzersiz_ekle_penceresi.egzersiz_eklendi_signal.connect(self.guncelle_egzersiz_tablosu)
        self.egzersiz_ekle_penceresi.setStyleSheet("background-color: rgb(40, 44, 52); color: white;")
        self.egzersiz_ekle_penceresi.show()

    def rapor_olustur(self):
        ad, yas, saglik_kaydi, egzersizler = self.kullanici.rapor_olustur()
        self.rapor_window = RaporPenceresi(self.kullanici.kullanici_adi, ad, yas, saglik_kaydi, egzersizler)
        self.rapor_window.setStyleSheet("background-color: rgb(40, 44, 52); color: white;")
        self.rapor_window.show()

    def guncelle_boy_kilo_tablosu(self, boy, kilo):
        rowPosition = self.saglik_kaydi_tablosu.rowCount()
        self.saglik_kaydi_tablosu.insertRow(rowPosition)
        self.saglik_kaydi_tablosu.setItem(rowPosition, 0, QTableWidgetItem(str(boy)))
        self.saglik_kaydi_tablosu.setItem(rowPosition, 1, QTableWidgetItem(str(kilo)))

    def guncelle_egzersiz_tablosu(self, egzersiz_adi, sure, tekrar_sayisi):
        rowPosition = self.egzersiz_tablosu.rowCount()
        self.egzersiz_tablosu.insertRow(rowPosition)
        self.egzersiz_tablosu.setItem(rowPosition, 0, QTableWidgetItem(egzersiz_adi))
        self.egzersiz_tablosu.setItem(rowPosition, 1, QTableWidgetItem(str(sure)))
        self.egzersiz_tablosu.setItem(rowPosition, 2, QTableWidgetItem(str(tekrar_sayisi)))

class Uygulama(QWidget):
    def __init__(self):
        super().__init__()

        self.hesaplar = {}  

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Kişisel Sağlık Takip Uygulaması')
        self.setGeometry(100, 100, 400, 300)

        self.login_button = QPushButton('Giriş Yap')
        self.login_button.clicked.connect(self.login)
        self.register_button = QPushButton('Hesap Oluştur')
        self.register_button.clicked.connect(self.register)

        layout = QVBoxLayout()
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register(self):
        self.register_window = HesapOlusturPenceresi(self.hesaplar)
        self.register_window.setStyleSheet("background-color: rgb(40, 44, 52); color: white;")
        self.register_window.hesap_olusturuldu_signal.connect(self.on_hesap_olusturuldu)
        self.register_window.show()

    def login(self):
        self.login_window = GirisYapPenceresi(self.hesaplar)
        self.login_window.setStyleSheet("background-color: rgb(40, 44, 52); color: white;")
        self.login_window.show()

    def on_hesap_olusturuldu(self, ad, yas):
        self.ana_ekran = AnaEkran(Kullanici("", "", ad, yas, ""))
        self.ana_ekran.setStyleSheet("background-color: rgb(40, 44, 52); color: white;")
        self.ana_ekran.show()

class HesapOlusturPenceresi(QWidget):
    hesap_olusturuldu_signal = pyqtSignal(str, int)

    def __init__(self, hesaplar):
        super().__init__()

        self.hesaplar = hesaplar

        self.setWindowTitle('Hesap Oluştur')
        self.setGeometry(200, 200, 300, 250)

        layout = QVBoxLayout()

        self.kullanici_adi_label = QLabel('Kullanıcı Adı:')
        self.kullanici_adi_input = QLineEdit()
        layout.addWidget(self.kullanici_adi_label)
        layout.addWidget(self.kullanici_adi_input)

        self.sifre_label = QLabel('Şifre:')
        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.Password)  
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre_input)

        self.ad_label = QLabel('Ad:')
        self.ad_input = QLineEdit()
        layout.addWidget(self.ad_label)
        layout.addWidget(self.ad_input)

        self.yas_label = QLabel('Yaş:')
        self.yas_input = QSpinBox()
        self.yas_input.setMinimum(1)
        self.yas_input.setMaximum(99)  
        layout.addWidget(self.yas_label)
        layout.addWidget(self.yas_input)

        self.cinsiyet_label = QLabel('Cinsiyet:')
        self.cinsiyet_combobox = QComboBox()
        self.cinsiyet_combobox.addItems(['ERKEK', 'KADIN', 'DİĞER'])
        layout.addWidget(self.cinsiyet_label)
        layout.addWidget(self.cinsiyet_combobox)

        self.kaydet_button = QPushButton('Kaydet')
        self.kaydet_button.clicked.connect(self.kullanici_kaydet)
        layout.addWidget(self.kaydet_button)

        self.setLayout(layout)

    def kullanici_kaydet(self):
        kullanici_adi = self.kullanici_adi_input.text()
        sifre = self.sifre_input.text()
        ad = self.ad_input.text()
        yas = self.yas_input.value()
        cinsiyet = self.cinsiyet_combobox.currentText()

        self.hesaplar[kullanici_adi] = sifre

        kullanici = Kullanici(kullanici_adi, sifre, ad, yas, cinsiyet)
        QMessageBox.information(self, 'Başarılı', 'Kullanıcı oluşturuldu: {}'.format(kullanici.kullanici_adi))

        self.hesap_olusturuldu_signal.emit(ad, yas)

class GirisYapPenceresi(QWidget):
    def __init__(self, hesaplar):
        super().__init__()

        self.hesaplar = hesaplar

        self.setWindowTitle('Giriş Yap')
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        self.kullanici_adi_label = QLabel('Kullanıcı Adı:')
        self.kullanici_adi_input = QLineEdit()
        layout.addWidget(self.kullanici_adi_label)
        layout.addWidget(self.kullanici_adi_input)

        self.sifre_label = QLabel('Şifre:')
        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.Password)  
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre_input)

        self.giris_button = QPushButton('Giriş Yap')
        self.giris_button.clicked.connect(self.giris_yap)
        layout.addWidget(self.giris_button)

        self.setLayout(layout)

    def giris_yap(self):
        kullanici_adi = self.kullanici_adi_input.text()
        sifre = self.sifre_input.text()
        
        if kullanici_adi in self.hesaplar and self.hesaplar[kullanici_adi] == sifre:
            QMessageBox.information(self, 'Başarılı', '{} kullanıcısı giriş yaptı.'.format(kullanici_adi))
            self.ana_ekran = AnaEkran(Kullanici(kullanici_adi, self.hesaplar[kullanici_adi], "", 0, ""))
            self.ana_ekran.setStyleSheet("background-color: rgb(40, 44, 52); color: white;")
            self.ana_ekran.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Hata', 'Geçersiz kullanıcı adı veya şifre.')

class SaglikKaydiPenceresi(QWidget):
    saglik_kaydi_signal = pyqtSignal(int, int)

    def __init__(self, kullanici):
        super().__init__()

        self.kullanici = kullanici

        self.setWindowTitle('Sağlık Kaydı Ekle')
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        self.boy_label = QLabel('Boy (cm):')
        self.boy_input = QLineEdit()
        self.boy_input.setValidator(QIntValidator(1, 250))  # Limiting height to 250 cm
        layout.addWidget(self.boy_label)
        layout.addWidget(self.boy_input)

        self.kilo_label = QLabel('Kilo (kg):')
        self.kilo_input = QLineEdit()
        self.kilo_input.setValidator(QIntValidator(1, 550))  # Limiting weight to 550 kg
        layout.addWidget(self.kilo_label)
        layout.addWidget(self.kilo_input)

        self.kaydet_button = QPushButton('Kaydet')
        self.kaydet_button.clicked.connect(self.kaydet)
        layout.addWidget(self.kaydet_button)

        self.setLayout(layout)

    def kaydet(self):
        boy = int(self.boy_input.text())
        kilo = int(self.kilo_input.text())

        self.kullanici.kayit_ekle((boy, kilo))

        self.saglik_kaydi_signal.emit(boy, kilo)
        self.close()

class EgzersizEklePenceresi(QWidget):
    egzersiz_eklendi_signal = pyqtSignal(str, int, int)

    def __init__(self, kullanici):
        super().__init__()

        self.kullanici = kullanici

        self.setWindowTitle('Egzersiz Ekle')
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.egzersiz_label = QLabel('Egzersiz Adı:')
        self.egzersiz_input = QLineEdit()
        layout.addWidget(self.egzersiz_label)
        layout.addWidget(self.egzersiz_input)

        self.sure_label = QLabel('Süre (dk):')
        self.sure_input = QLineEdit()
        layout.addWidget(self.sure_label)
        layout.addWidget(self.sure_input)

        self.tekrar_label = QLabel('Tekrar Sayısı:')
        self.tekrar_input = QLineEdit()
        layout.addWidget(self.tekrar_label)
        layout.addWidget(self.tekrar_input)

        self.kaydet_button = QPushButton('Kaydet')
        self.kaydet_button.clicked.connect(self.kaydet)
        layout.addWidget(self.kaydet_button)

        self.setLayout(layout)

    def kaydet(self):
        egzersiz_adi = self.egzersiz_input.text()
        sure = int(self.sure_input.text())
        tekrar_sayisi = int(self.tekrar_input.text())

        self.kullanici.egzersiz_ekle((egzersiz_adi, sure, tekrar_sayisi))

        self.egzersiz_eklendi_signal.emit(egzersiz_adi, sure, tekrar_sayisi)
        self.close()

class RaporPenceresi(QWidget):
    def __init__(self, kullanici_adi, ad, yas, saglik_kaydi, egzersizler):
        super().__init__()

        self.setWindowTitle('Kullanıcı Raporu - {}'.format(kullanici_adi))
        self.setGeometry(200, 200, 500, 300)

        layout = QVBoxLayout()

        self.ad_label = QLabel('Ad: {}'.format(ad))
        layout.addWidget(self.ad_label)

        self.yas_label = QLabel('Yaş: {}'.format(yas))
        layout.addWidget(self.yas_label)

        self.saglik_kaydi_label = QLabel('Sağlık Kaydı:')
        layout.addWidget(self.saglik_kaydi_label)

        self.saglik_kaydi_table = QTableWidget()
        self.saglik_kaydi_table.setColumnCount(2)  
        self.saglik_kaydi_table.setHorizontalHeaderLabels(["Boy (cm)", "Kilo (kg)"])
        self.saglik_kaydi_table.setRowCount(len(saglik_kaydi))  
        for i, kayit in enumerate(saglik_kaydi):
            self.saglik_kaydi_table.setItem(i, 0, QTableWidgetItem(str(kayit[0])))
            self.saglik_kaydi_table.setItem(i, 1, QTableWidgetItem(str(kayit[1])))
        self.saglik_kaydi_table.horizontalHeader().setStyleSheet("color: black;")
        layout.addWidget(self.saglik_kaydi_table)

        self.egzersiz_label = QLabel('Egzersizler:')
        layout.addWidget(self.egzersiz_label)

        self.egzersiz_table = QTableWidget()
        self.egzersiz_table.setColumnCount(3)  
        self.egzersiz_table.setHorizontalHeaderLabels(["Egzersiz Adı", "Süre (dk)", "Tekrar Sayısı"])
        self.egzersiz_table.setRowCount(len(egzersizler))  
        for i, egzersiz in enumerate(egzersizler):
            self.egzersiz_table.setItem(i, 0, QTableWidgetItem(egzersiz[0]))
            self.egzersiz_table.setItem(i, 1, QTableWidgetItem(str(egzersiz[1])))
            self.egzersiz_table.setItem(i, 2, QTableWidgetItem(str(egzersiz[2])))
        self.egzersiz_table.horizontalHeader().setStyleSheet("color: black;")
        layout.addWidget(self.egzersiz_table)

        self.setLayout(layout)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    uygulama = Uygulama()
    uygulama.setStyleSheet("background-color: rgb(40, 44, 52); color: white;")
    uygulama.show()
    sys.exit(app.exec_())
