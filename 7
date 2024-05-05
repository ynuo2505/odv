import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class GirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Giriş Ekranı')
        self.setGeometry(100, 100, 800, 650)

        self.label_kullanici_adi = QLabel('Kullanıcı Adı:')
        self.input_kullanici_adi = QLineEdit()

        self.label_sifre = QLabel('Şifre:')
        self.input_sifre = QLineEdit()
        self.input_sifre.setEchoMode(QLineEdit.Password)

        self.button_giris = QPushButton('Giriş Yap')
        self.button_giris.clicked.connect(self.giris_yap)

        self.button_kayit = QPushButton('Kayıt Ol')
        self.button_kayit.clicked.connect(self.ac_kayit_ekrani)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label_kullanici_adi)
        self.layout.addWidget(self.input_kullanici_adi)
        self.layout.addWidget(self.label_sifre)
        self.layout.addWidget(self.input_sifre)
        self.layout.addWidget(self.button_giris)
        self.layout.addWidget(self.button_kayit)

        self.setLayout(self.layout)

    def giris_yap(self):
        kullanici_adi = self.input_kullanici_adi.text()
        sifre = self.input_sifre.text()

        # Kullanıcı adı ve şifre dolu mu kontrol et
        if kullanici_adi and sifre:
            self.hide()
            self.antrenmanlar_sayfasi = ListeSayfasi()
            self.antrenmanlar_sayfasi.show()
        else:
            QMessageBox.warning(self, 'Hata', 'Kullanıcı adı ve şifre alanları boş olamaz!')

    def ac_kayit_ekrani(self):
        self.hide()
        self.kayit_ekrani = KayitEkrani(self)
        self.kayit_ekrani.show()


class KayitEkrani(QWidget):
    def __init__(self, previous_window):
        super().__init__()
        self.previous_window = previous_window
        self.setWindowTitle('Kayıt Ekranı')
        self.setGeometry(100, 100, 800, 650)

        self.label_ad = QLabel('Ad:')
        self.input_ad = QLineEdit()
        self.label_soyad = QLabel('Soyad:')
        self.input_soyad = QLineEdit()
        self.label_kimlik_no = QLabel('Kimlik No (11 Haneli):')
        self.input_kimlik_no = QLineEdit()
        self.input_kimlik_no.setMaxLength(11)
        self.label_kimlik_no.setToolTip('Kimlik numarası 11 haneli olmalıdır.')
        self.label_spor_dali = QLabel('Spor Dalı:')
        self.input_spor_dali = QLineEdit()
        self.label_sifre = QLabel('Şifre:')
        self.input_sifre = QLineEdit()
        self.input_sifre.setEchoMode(QLineEdit.Password)

        self.button_kayit = QPushButton('Kayıt Ol')
        self.button_kayit.clicked.connect(self.kayit_ol)

        self.button_geri_don = QPushButton('Geri Dön')
        self.button_geri_don.clicked.connect(self.geri_don)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label_ad)
        self.layout.addWidget(self.input_ad)
        self.layout.addWidget(self.label_soyad)
        self.layout.addWidget(self.input_soyad)
        self.layout.addWidget(self.label_kimlik_no)
        self.layout.addWidget(self.input_kimlik_no)
        self.layout.addWidget(self.label_spor_dali)
        self.layout.addWidget(self.input_spor_dali)
        self.layout.addWidget(self.label_sifre)
        self.layout.addWidget(self.input_sifre)
        self.layout.addWidget(self.button_kayit)
        self.layout.addWidget(self.button_geri_don)

        self.setLayout(self.layout)

    def kayit_ol(self):
        ad = self.input_ad.text()
        soyad = self.input_soyad.text()
        kimlik_no = self.input_kimlik_no.text()
        spor_dali = self.input_spor_dali.text()
        sifre = self.input_sifre.text()

        if len(kimlik_no) != 11:
            QMessageBox.warning(self, 'Hata', 'Kimlik numarası 11 haneli olmalıdır!')
            return

        if ad and soyad and spor_dali and sifre:
            QMessageBox.information(self, 'Başarılı', 'Kayıt başarıyla oluşturuldu.')
            self.clear_input()
        else:
            QMessageBox.warning(self, 'Hata', 'Ad, Soyad, Spor Dalı ve Şifre alanları boş bırakılamaz!')

    def clear_input(self):
        self.input_ad.clear()
        self.input_soyad.clear()
        self.input_kimlik_no.clear()
        self.input_spor_dali.clear()
        self.input_sifre.clear()

    def geri_don(self):
        self.close()
        self.previous_window.show()


class ListeSayfasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Liste Sayfası')
        self.setGeometry(100, 100, 800, 650)

        self.label_baslik = QLabel('Liste Sayfası')
        self.label_baslik.setAlignment(Qt.AlignCenter)

        self.button_antrenman_olustur = QPushButton('Antrenman Oluştur')
        self.button_antrenman_olustur.clicked.connect(self.ac_antrenman_olustur_sayfasi)

        self.button_geri_don = QPushButton('Geri Dön')
        self.button_geri_don.clicked.connect(self.geri_don)

        self.button_yapildi = QPushButton('Yapıldı!')
        self.button_yapildi.clicked.connect(self.yapildi)

        self.table_sol = QTableWidget()
        self.table_sol.setColumnCount(1)
        self.table_sol.setHorizontalHeaderLabels(['Yapılacak listeniz'])

        self.table_sag = QTableWidget()
        self.table_sag.setColumnCount(1)
        self.table_sag.setHorizontalHeaderLabels(['Yapılanlar'])

        layout = QHBoxLayout()
        layout.addWidget(self.table_sol)
        layout.addWidget(self.table_sag)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label_baslik)
        main_layout.addLayout(layout)
        main_layout.addWidget(self.button_antrenman_olustur)
        main_layout.addWidget(self.button_geri_don)
        main_layout.addWidget(self.button_yapildi)

        self.setLayout(main_layout)

    def ac_antrenman_olustur_sayfasi(self):
        self.hide()
        self.antrenman_olustur_sayfasi = AntrenmanOlusturSayfasi()
        self.antrenman_olustur_sayfasi.previous_window = self
        self.antrenman_olustur_sayfasi.show()

    def geri_don(self):
        self.close()
        self.previous_window = GirisEkrani()
        self.previous_window.show()

    def yapildi(self):
        selected_items = self.table_sol.selectedItems()
        for item in selected_items:
            exercise = item.text()
            row_count = self.table_sag.rowCount()
            self.table_sag.insertRow(row_count)
            self.table_sag.setItem(row_count, 0, QTableWidgetItem(exercise))
            self.table_sol.removeRow(item.row())

        if self.table_sol.rowCount() == 0:
            QMessageBox.information(self, 'Tebrikler!', 'Tüm antrenmanlarınızı tamamladınız!')


class AntrenmanOlusturSayfasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Antrenman Oluştur')
        self.setGeometry(100, 100, 800, 650)

        self.label_baslik = QLabel('Antrenman Oluştur Sayfası')
        self.label_baslik.setAlignment(Qt.AlignCenter)

        self.button_geri_don = QPushButton('Geri Dön')
        self.button_geri_don.clicked.connect(self.geri_don)

        self.table_antrenmanlar = QTableWidget()
        self.table_antrenmanlar.setColumnCount(1)
        self.table_antrenmanlar.setHorizontalHeaderLabels(['Antrenman'])

        self.table_listem = QTableWidget()
        self.table_listem.setColumnCount(1)
        self.table_listem.setHorizontalHeaderLabels(['Önerilen Hareketler'])

        self.table_sag_liste = QTableWidget()
        self.table_sag_liste.setColumnCount(1)
        self.table_sag_liste.setHorizontalHeaderLabels(['Listeniz'])

        self.button_ekle = QPushButton('Ekle')
        self.button_ekle.clicked.connect(self.ekle)
        self.button_cikart = QPushButton('Çıkart')
        self.button_cikart.clicked.connect(self.cikart)

        self.button_kaydet = QPushButton('Listeyi Kaydet')
        self.button_kaydet.clicked.connect(self.kaydet)

        kategoriler = ["Ön Kol", "Arka Kol", "Göğüs", "Bacak"]

        for kategori in kategoriler:
            self.table_antrenmanlar.insertRow(self.table_antrenmanlar.rowCount())
            self.table_antrenmanlar.setItem(self.table_antrenmanlar.rowCount() - 1, 0, QTableWidgetItem(kategori))

        self.table_antrenmanlar.itemClicked.connect(self.ekle_antrenman)

        layout = QHBoxLayout()
        layout.addWidget(self.table_antrenmanlar)
        layout.addWidget(self.table_listem)
        layout.addWidget(self.table_sag_liste)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label_baslik)
        main_layout.addLayout(layout)
        main_layout.addWidget(self.button_ekle)
        main_layout.addWidget(self.button_cikart)
        main_layout.addWidget(self.button_kaydet)
        main_layout.addWidget(self.button_geri_don)

        self.setLayout(main_layout)

        self.selected_exercises = set()

    def ekle_antrenman(self, item):
        onerilen_hareketler = {
            "Göğüs": ["Bench Press", "Dumbbell Fly", "Chest Dip", "Şınav"],
            "Ön Kol": ["Biceps Curl", "Hammer Curl", "Wrist Curl"],
            "Arka Kol": ["Triceps Extension", "Triceps Kickback", "Dips"],
            "Bacak": ["Squat", "Deadlift", "Leg Press"]
        }

        kategori = item.text()

        self.table_listem.setRowCount(0)
        for hareket in onerilen_hareketler.get(kategori, []):
            if hareket not in self.selected_exercises:
                row_count = self.table_listem.rowCount()
                self.table_listem.insertRow(row_count)
                self.table_listem.setItem(row_count, 0, QTableWidgetItem(hareket))

    def ekle(self):
        selected_items = self.table_listem.selectedItems()
        for item in selected_items:
            exercise = item.text()
            if exercise not in self.selected_exercises:
                row_count = self.table_sag_liste.rowCount()
                self.table_sag_liste.insertRow(row_count)
                self.table_sag_liste.setItem(row_count, 0, QTableWidgetItem(exercise))
                self.selected_exercises.add(exercise)

    def cikart(self):
        selected_items = self.table_sag_liste.selectedItems()
        for item in selected_items:
            exercise = item.text()
            row = self.table_sag_liste.row(item)
            self.table_sag_liste.removeRow(row)
            self.selected_exercises.remove(exercise)

    def kaydet(self):
        saved_exercises = [self.table_sag_liste.item(row, 0).text() for row in range(self.table_sag_liste.rowCount())]
        QMessageBox.information(self, 'Kaydedildi', f'Seçilen hareketler: {", ".join(saved_exercises)}')

        self.previous_window.table_sol.setRowCount(0)
        for hareket in saved_exercises:
            row_count = self.previous_window.table_sol.rowCount()
            self.previous_window.table_sol.insertRow(row_count)
            self.previous_window.table_sol.setItem(row_count, 0, QTableWidgetItem(hareket))

    def geri_don(self):
        self.close()
        self.previous_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GirisEkrani()
    window.show()
    sys.exit(app.exec_())
