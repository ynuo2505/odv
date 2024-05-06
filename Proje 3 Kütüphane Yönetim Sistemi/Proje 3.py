import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QStackedWidget, QHBoxLayout, QHeaderView

class GirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Kullanıcı Girişi')
        self.setGeometry(400, 600, 700, 200)

        layout = QVBoxLayout()

        self.ad_soyad_label = QLabel("Ad Soyad:")
        self.ad_soyad_girdi = QLineEdit()
        layout.addWidget(self.ad_soyad_label)
        layout.addWidget(self.ad_soyad_girdi)

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
        self.giris_buton.setStyleSheet("background-color: #34495e; color: white; border: 1px solid #34495e;")
        self.giris_buton.clicked.connect(self.giris)
        layout.addWidget(self.giris_buton)

        self.kayit_ol_buton = QPushButton("Kayıt Ol")
        self.kayit_ol_buton.setStyleSheet("background-color: #2c3e50; color: white; border: 1px solid #2c3e50;")
        self.kayit_ol_buton.clicked.connect(self.kayit_ol)
        layout.addWidget(self.kayit_ol_buton)

        self.setLayout(layout)

        self.kullanicilar = {}  # Kullanıcı adı ve şifrelerin saklandığı sözlük

    def giris(self):
        kullanici_adi = self.kullanici_adi_girdi.text()
        sifre = self.sifre_girdi.text()

        if kullanici_adi in self.kullanicilar and self.kullanicilar[kullanici_adi]['sifre'] == sifre:
            self.acilis_penceresini_goster()
        else:
            QMessageBox.warning(self, 'Uyarı', 'Geçersiz kullanıcı adı veya şifre!')

    def kayit_ol(self):
        ad_soyad = self.ad_soyad_girdi.text()
        kullanici_adi = self.kullanici_adi_girdi.text()
        sifre = self.sifre_girdi.text()

        if ad_soyad and kullanici_adi and sifre:
            if kullanici_adi not in self.kullanicilar:
                self.kullanicilar[kullanici_adi] = {'ad_soyad': ad_soyad, 'sifre': sifre}
                QMessageBox.information(self, 'Bilgi', 'Kayıt başarıyla tamamlandı!')
            else:
                QMessageBox.warning(self, 'Uyarı', 'Bu kullanıcı zaten mevcut!')
        else:
            QMessageBox.warning(self, 'Uyarı', 'Tüm alanlar doldurulmalıdır!')

    def acilis_penceresini_goster(self):
        self.acilis_penceresi = AnaPencere()
        self.acilis_penceresi.show()
        self.close()

class AnaPencere(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.ana_ekran = AnaEkran()
        self.addWidget(self.ana_ekran)

class AnaEkran(QWidget):
    def __init__(self):
        super().__init__()
        self.kitaplar = self.random_kitaplar_olustur(30)
        self.odunc_alinan_kitaplar = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.buton_1 = QPushButton('Kitap Ara')
        self.buton_1.setStyleSheet("background-color: #34495e; color: white; border: 1px solid #34495e;")
        self.buton_1.clicked.connect(self.kitap_ara)
        layout.addWidget(self.buton_1)

        self.buton_2 = QPushButton('Çıkış')
        self.buton_2.setStyleSheet("background-color: #2c3e50; color: white; border: 1px solid #2c3e50;")
        self.buton_2.clicked.connect(self.cikis)
        layout.addWidget(self.buton_2)

        # Table to display all books
        self.kitaplar_tablosu = QTableWidget()
        self.kitaplar_tablosu.setColumnCount(4)
        self.kitaplar_tablosu.setHorizontalHeaderLabels(['Kitap Adı', 'Yazar', 'Durum', 'İşlem'])
        self.kitaplar_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.kitaplar_tablosu)

        # Table to display borrowed books
        self.odunc_tablosu = QTableWidget()
        self.odunc_tablosu.setColumnCount(3)
        self.odunc_tablosu.setHorizontalHeaderLabels(['Kitap Adı', 'Yazar', 'Durum'])
        self.odunc_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(QLabel('Ödünç Alınan Kitaplar:'))
        layout.addWidget(self.odunc_tablosu)

        self.iade_button = QPushButton('Kitap İade Et')
        self.iade_button.setStyleSheet("background-color: #2c3e50; color: white; border: 1px solid #2c3e50;")
        self.iade_button.clicked.connect(self.kitap_iade)
        layout.addWidget(self.iade_button)

        self.populate_kitaplar_tablosu()

        self.setLayout(layout)

    def populate_kitaplar_tablosu(self):
        self.kitaplar_tablosu.setRowCount(0)
        for kitap in self.kitaplar:
            row_position = self.kitaplar_tablosu.rowCount()
            self.kitaplar_tablosu.insertRow(row_position)
            for col, data in enumerate(kitap.values()):
                self.kitaplar_tablosu.setItem(row_position, col, QTableWidgetItem(str(data)))
            borrow_button = QPushButton('Ödünç Al')
            borrow_button.setStyleSheet("background-color: #2c3e50; color: white; border: 1px solid #2c3e50;")
            borrow_button.clicked.connect(lambda _, kitap=kitap: self.odunc_al_kitap(kitap))
            self.kitaplar_tablosu.setCellWidget(row_position, 3, borrow_button)

    def random_kitaplar_olustur(self, count):
        kitaplar = [
            {'ad': 'Suç ve Ceza', 'yazar': 'Fyodor Dostoyevski', 'durum': 'Mevcut'},
            {'ad': '1984', 'yazar': 'George Orwell', 'durum': 'Mevcut'},
            {'ad': 'Bülbülü Öldürmek', 'yazar': 'Harper Lee', 'durum': 'Mevcut'},
            {'ad': 'Kürk Mantolu Madonna', 'yazar': 'Sabahattin Ali', 'durum': 'Mevcut'},
            {'ad': 'Yüzyıllık Yalnızlık', 'yazar': 'Gabriel García Márquez', 'durum': 'Mevcut'},
            {'ad': 'Olasılıksız', 'yazar': 'Adam Fawer', 'durum': 'Mevcut'},
            {'ad': 'Sefiller', 'yazar': 'Victor Hugo', 'durum': 'Mevcut'},
            {'ad': 'Harry Potter ve Felsefe Taşı', 'yazar': 'J.K. Rowling', 'durum': 'Mevcut'},
            {'ad': 'Göğüs Kafesi', 'yazar': 'Nihan İpek', 'durum': 'Mevcut'},
            {'ad': 'Beyaz Zambaklar Ülkesinde', 'yazar': 'Grigory Petrov', 'durum': 'Mevcut'},
            {'ad': 'Dorian Gray\'in Portresi', 'yazar': 'Oscar Wilde', 'durum': 'Mevcut'},
            {'ad': 'Karamazov Kardeşler', 'yazar': 'Fyodor Dostoyevski', 'durum': 'Mevcut'},
            {'ad': 'Simyacı', 'yazar': 'Paulo Coelho', 'durum': 'Mevcut'},
            {'ad': 'Aşk', 'yazar': 'Elif Şafak', 'durum': 'Mevcut'},
            {'ad': 'Savaş ve Barış', 'yazar': 'Lev Tolstoy', 'durum': 'Mevcut'},
            {'ad': 'İstanbul Hatırası', 'yazar': 'Ahmet Ümit', 'durum': 'Mevcut'},
            {'ad': 'Bilinmeyen Bir Kadının Mektubu', 'yazar': 'Stefan Zweig', 'durum': 'Mevcut'},
            {'ad': 'Çalıkuşu', 'yazar': 'Reşat Nuri Güntekin', 'durum': 'Mevcut'},
            {'ad': 'Dracula', 'yazar': 'Bram Stoker', 'durum': 'Mevcut'},
            {'ad': 'Sis ve Gece', 'yazar': 'Ahmet Ümit', 'durum': 'Mevcut'},
            {'ad': 'Küçük Prens', 'yazar': 'Antoine de Saint-Exupéry', 'durum': 'Mevcut'},
            {'ad': 'Martı', 'yazar': 'Richard Bach', 'durum': 'Mevcut'},
            {'ad': 'İnci', 'yazar': 'John Steinbeck', 'durum': 'Mevcut'},
            {'ad': 'Aynanın İçinden', 'yazar': 'Fyodor Dostoyevski', 'durum': 'Mevcut'},
            {'ad': 'Vadideki Zambak', 'yazar': 'Honoré de Balzac', 'durum': 'Mevcut'},
            {'ad': 'Bir Delinin Hatıra Defteri', 'yazar': 'Nikolay Gogol', 'durum': 'Mevcut'},
            {'ad': 'İnce Memed', 'yazar': 'Yaşar Kemal', 'durum': 'Mevcut'},
            {'ad': 'Uçurtma Avcısı', 'yazar': 'Khaled Hosseini', 'durum': 'Mevcut'},
            {'ad': 'Sineklerin Tanrısı', 'yazar': 'William Golding', 'durum': 'Mevcut'},
        ]
        return kitaplar[:count]

    def kitap_ara(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Kitap Ara')
        dialog.setGeometry(300, 300, 500, 300)

        layout = QVBoxLayout()

        kitap_ara_label = QLabel('Kitap Adı:')
        layout.addWidget(kitap_ara_label)

        kitap_ara_input = QLineEdit()
        layout.addWidget(kitap_ara_input)

        kitaplar_tablosu = QTableWidget()
        kitaplar_tablosu.setColumnCount(4)
        kitaplar_tablosu.setHorizontalHeaderLabels(['Kitap Adı', 'Yazar', 'Durum', 'İşlem'])
        kitaplar_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(kitaplar_tablosu)

        def kitap_ara():
            search_text = kitap_ara_input.text().lower()
            if search_text:
                filtered_kitaplar = [kitap for kitap in self.kitaplar if search_text in kitap['ad'].lower()]
                kitaplar_tablosu.setRowCount(0)
                for row, kitap in enumerate(filtered_kitaplar):
                    kitaplar_tablosu.insertRow(row)
                    for col, data in enumerate(kitap.values()):
                        kitaplar_tablosu.setItem(row, col, QTableWidgetItem(str(data)))
                    borrow_button = QPushButton('Ödünç Al')
                    borrow_button.setStyleSheet("background-color: #2c3e50; color: white; border: 1px solid #2c3e50;")
                    borrow_button.clicked.connect(lambda _, kitap=kitap: self.odunc_al_kitap(kitap))
                    kitaplar_tablosu.setCellWidget(row, 3, borrow_button)
            else:
                kitaplar_tablosu.setRowCount(0)

        kitap_ara_button = QPushButton('Ara')
        kitap_ara_button.setStyleSheet("background-color: #34495e; color: white; border: 1px solid #34495e;")
        kitap_ara_button.clicked.connect(kitap_ara)
        layout.addWidget(kitap_ara_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def cikis(self):
        sys.exit()

    def odunc_al_kitap(self, kitap):
        if kitap not in self.odunc_alinan_kitaplar:
            kitap['durum'] = 'Ödünç Alındı'
            self.odunc_alinan_kitaplar.append(kitap)
            self.populate_kitaplar_tablosu()
            self.populate_odunc_tablosu()  # Add this line
            QMessageBox.information(self, 'Bilgi', f"{kitap['ad']} adlı kitap ödünç alındı.")
        else:
            QMessageBox.warning(self, 'Uyarı', 'Bu kitap zaten ödünç alınmış.')

    def kitap_iade(self):
        selected_rows = set()
        for item in self.odunc_tablosu.selectedItems():
            selected_rows.add(item.row())

        for row in sorted(selected_rows, reverse=True):
            returned_book = self.odunc_alinan_kitaplar.pop(row)
            returned_book['durum'] = 'Mevcut'
            self.populate_kitaplar_tablosu()
            QMessageBox.information(self, 'Bilgi', f"{returned_book['ad']} adlı kitap iade edildi.")

        self.populate_odunc_tablosu()

    def populate_odunc_tablosu(self):
        self.odunc_tablosu.setRowCount(0)
        for kitap in self.odunc_alinan_kitaplar:
            row_position = self.odunc_tablosu.rowCount()
            self.odunc_tablosu.insertRow(row_position)
            for col, data in enumerate(kitap.values()):
                self.odunc_tablosu.setItem(row_position, col, QTableWidgetItem(str(data)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Set Fusion style
    app.setPalette(app.style().standardPalette())  # Apply Fusion palette
    giris_ekrani = GirisEkrani()
    giris_ekrani.show()
    sys.exit(app.exec_())
