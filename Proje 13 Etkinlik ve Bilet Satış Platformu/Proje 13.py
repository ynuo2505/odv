import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QHeaderView
import random

class AnaEkran(QWidget):
    def __init__(self):
        super().__init__()
        self.etkinlikler = self.random_etkinlikler_olustur(20)
        self.kayitli_etkinlikler = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Etkinlik Takip Sistemi')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QVBoxLayout()

        self.buton_1 = QPushButton('Etkinlik Ara')
        self.buton_1.setStyleSheet("background-color: #3498db; color: white; border: 1px solid #3498db;")
        self.buton_1.clicked.connect(self.etkinlik_ara)
        layout.addWidget(self.buton_1)

        self.buton_2 = QPushButton('Çıkış')
        self.buton_2.setStyleSheet("background-color: #2ecc71; color: white; border: 1px solid #2ecc71;")
        self.buton_2.clicked.connect(self.cikis)
        layout.addWidget(self.buton_2)

        # Table to display all events
        self.etkinlikler_tablosu = QTableWidget()
        self.etkinlikler_tablosu.setColumnCount(5)
        self.etkinlikler_tablosu.setHorizontalHeaderLabels(['Etkinlik Adı', 'Yapımcı', 'Bilet Durumu', 'Türü','İşlem'])
        self.etkinlikler_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.etkinlikler_tablosu)

        # Table to display registered events
        self.kayitli_etkinlikler_tablosu = QTableWidget()
        self.kayitli_etkinlikler_tablosu.setColumnCount(3)
        self.kayitli_etkinlikler_tablosu.setHorizontalHeaderLabels(['Etkinlik Adı', 'Yapımcı', 'Bilet Durumu'])
        self.kayitli_etkinlikler_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(QLabel('Satın Alınan Biletler:'))
        layout.addWidget(self.kayitli_etkinlikler_tablosu)

        # Unregister button for registered events
        self.iade_button = QPushButton('Bileti İade Et')
        self.iade_button.setStyleSheet("background-color: #2ecc71; color: white; border: 1px solid #2ecc71;")
        self.iade_button.clicked.connect(self.etkinlik_iade)
        layout.addWidget(self.iade_button)

        # Populate table with all events
        self.populate_etkinlikler_tablosu()

        self.setLayout(layout)

    def populate_etkinlikler_tablosu(self):
        self.etkinlikler_tablosu.setRowCount(0)
        for etkinlik in self.etkinlikler:
            row_position = self.etkinlikler_tablosu.rowCount()
            self.etkinlikler_tablosu.insertRow(row_position)
            for col, data in enumerate(etkinlik.values()):
                self.etkinlikler_tablosu.setItem(row_position, col, QTableWidgetItem(str(data)))
            register_button = QPushButton('Satın Al')
            register_button.setStyleSheet("background-color: #2ecc71; color: white; border: 1px solid #2ecc71;")
            register_button.clicked.connect(lambda _, etkinlik=etkinlik: self.etkinlik_kaydet(etkinlik))
            self.etkinlikler_tablosu.setCellWidget(row_position, 4, register_button)

    def random_etkinlikler_olustur(self, count):
        etkinlikler = []

        film_etkinlikleri = [
            {'ad': 'Matrix', 'yazar': 'Lana Wachowski, Lilly Wachowski', 'durum': 'Vizyonda', 'Türü': 'Film'},
            {'ad': 'Yüzüklerin Efendisi: Yüzük Kardeşliği', 'yazar': 'Peter Jackson', 'durum': 'Vizyonda', 'Türü': 'Film'},
            {'ad': 'Başlangıç', 'yazar': 'Christopher Nolan', 'durum': 'Vizyonda', 'Türü': 'Film'},
            {'ad': 'Efsane', 'yazar': 'Ridley Scott', 'durum': 'Vizyonda', 'Türü': 'Film'},
            {'ad': 'Gizemli Nehir', 'yazar': 'Clint Eastwood', 'durum': 'Vizyonda', 'Türü': 'Film'},
            {'ad': 'Yeşil Yol', 'yazar': 'Frank Darabont', 'durum': 'Vizyonda', 'Türü': 'Film'},
            {'ad': 'Sonsuzluk Teorisi', 'yazar': 'James Marsh', 'durum': 'Vizyonda', 'Türü': 'Film'},
            {'ad': 'Efsanevi Doğuş', 'yazar': 'Christopher Nolan', 'durum': 'Vizyonda', 'Türü': 'Film'},
            {'ad': 'Schindler\'in Listesi', 'yazar': 'Steven Spielberg', 'durum': 'Vizyonda', 'Türü': 'Film'},
            {'ad': 'Gladyatör', 'yazar': 'David Franzoni', 'durum': 'Vizyonda', 'Türü': 'Film'},
        ]

        tiyatro_etkinlikleri = [
            {'ad': 'Kral Lear', 'yazar': 'William Shakespeare', 'durum': 'Vizyonda', 'Türü': 'Tiyatro'},
            {'ad': 'Hamlet', 'yazar': 'William Shakespeare', 'durum': 'Vizyonda', 'Türü': 'Tiyatro'},
            {'ad': 'Macbeth', 'yazar': 'William Shakespeare', 'durum': 'Vizyonda', 'Türü': 'Tiyatro'},
            {'ad': 'Çehov Makinesi', 'yazar': 'Anton Pavloviç Çehov', 'durum': 'Vizyonda', 'Türü': 'Tiyatro'},
            {'ad': 'Ay Işığında Şamata', 'yazar': 'Eugene O\'Neill', 'durum': 'Vizyonda', 'Türü': 'Tiyatro'},
            {'ad': 'Uçurtma Avcısı', 'yazar': 'Khaled Hosseini', 'durum': 'Vizyonda', 'Türü': 'Tiyatro'},
            {'ad': 'Danton\'un Ölümü', 'yazar': 'Georg Büchner', 'durum': 'Vizyonda', 'Türü': 'Tiyatro'},
            {'ad': 'Otello', 'yazar': 'William Shakespeare', 'durum': 'Vizyonda', 'Türü': 'Tiyatro'},
            {'ad': 'Şeytan Dışarıda', 'yazar': 'Jean-Paul Sartre', 'durum': 'Vizyonda', 'Türü': 'Tiyatro'},
            {'ad': 'Fareler ve İnsanlar', 'yazar': 'John Steinbeck', 'durum': 'Vizyonda', 'Türü': 'Tiyatro'},
        ]

        # Rastgele 10 film etkinliği ekle
        etkinlikler.extend(random.sample(film_etkinlikleri, 10))

        # Rastgele 10 tiyatro etkinliği ekle
        etkinlikler.extend(random.sample(tiyatro_etkinlikleri, 10))

        return etkinlikler[:count]

    def etkinlik_ara(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Etkinlik Ara')
        dialog.setGeometry(300, 300, 500, 300)

        layout = QVBoxLayout()

        etkinlik_ara_label = QLabel('Etkinlik Adı:')
        layout.addWidget(etkinlik_ara_label)

        etkinlik_ara_input = QLineEdit()
        layout.addWidget(etkinlik_ara_input)

        etkinlikler_tablosu = QTableWidget()
        etkinlikler_tablosu.setColumnCount(5)
        etkinlikler_tablosu.setHorizontalHeaderLabels(['Etkinlik Adı', 'Yapımcı', 'Bilet Durumu', 'Türü', 'İşlem'])
        etkinlikler_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(etkinlikler_tablosu)

        def etkinlik_ara():
            search_text = etkinlik_ara_input.text().lower()
            if search_text:
                filtered_etkinlikler = [etkinlik for etkinlik in self.etkinlikler if search_text in etkinlik['ad'].lower()]
                etkinlikler_tablosu.setRowCount(0)
                for row, etkinlik in enumerate(filtered_etkinlikler):
                    etkinlikler_tablosu.insertRow(row)
                    for col, data in enumerate(etkinlik.values()):
                        etkinlikler_tablosu.setItem(row, col, QTableWidgetItem(str(data)))
                    register_button = QPushButton('Satın Al')
                    register_button.setStyleSheet("background-color: #2ecc71; color: white; border: 1px solid #2ecc71;")
                    register_button.clicked.connect(lambda _, etkinlik=etkinlik: self.etkinlik_kaydet(etkinlik))
                    etkinlikler_tablosu.setCellWidget(row, 4, register_button)
            else:
                etkinlikler_tablosu.setRowCount(0)

        etkinlik_ara_button = QPushButton('Ara')
        etkinlik_ara_button.clicked.connect(etkinlik_ara)
        layout.addWidget(etkinlik_ara_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def cikis(self):
        sys.exit()

    def etkinlik_kaydet(self, etkinlik):
        if etkinlik not in self.kayitli_etkinlikler:
            etkinlik['durum'] = 'Satın Alındı'
            self.kayitli_etkinlikler.append(etkinlik)
            self.populate_etkinlikler_tablosu()
            self.populate_kayitli_etkinlikler_tablosu()
            QMessageBox.information(self, 'Bilgi', f"{etkinlik['ad']} adlı bilet satın alındı.")
        else:
            QMessageBox.warning(self, 'Uyarı', 'Bu bilet zaten satın alınmış.')

    def etkinlik_iade(self):
        selected_rows = set()
        for item in self.kayitli_etkinlikler_tablosu.selectedItems():
            selected_rows.add(item.row())

        for row in sorted(selected_rows, reverse=True):
            returned_event = self.kayitli_etkinlikler.pop(row)
            returned_event['durum'] = 'Vizyonda'
            self.populate_etkinlikler_tablosu()

        self.populate_kayitli_etkinlikler_tablosu()
        QMessageBox.information(self, 'Bilgi', f"{returned_event['ad']} adlı biletiniz iade edildi.")

    def populate_kayitli_etkinlikler_tablosu(self):
        self.kayitli_etkinlikler_tablosu.setRowCount(0)
        for etkinlik in self.kayitli_etkinlikler:
            row_position = self.kayitli_etkinlikler_tablosu.rowCount()
            self.kayitli_etkinlikler_tablosu.insertRow(row_position)
            for col, data in enumerate(etkinlik.values()):
                self.kayitli_etkinlikler_tablosu.setItem(row_position, col, QTableWidgetItem(str(data)))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ana_ekran = AnaEkran()

    ana_ekran.show()

    sys.exit(app.exec_())
