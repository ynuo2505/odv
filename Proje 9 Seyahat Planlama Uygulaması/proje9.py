import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QSpinBox, QComboBox, QHBoxLayout, QSlider, QStackedWidget
from PyQt5.QtCore import Qt

class Konaklama:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

class Rota:
    def __init__(self, details, seyahat_suresi):
        self.details = details
        self.seyahat_suresi = seyahat_suresi
        self.konaklama_secenekleri = []
        self.notes = []

    def konaklama_ekle(self, konaklama):
        self.konaklama_secenekleri.append(konaklama)

    def add_note(self, note):
        self.notes.append(note)

class Seyahat:
    def __init__(self):
        self.rotalar = []
        self.konaklamalar = []

    def rota_ekle(self, rota):
        self.rotalar.append(rota)

    def konaklama_ekle(self, konaklama):
        self.konaklamalar.append(konaklama)

    def seyahat_sil(self, rota):
        for r in self.rotalar:
            if r.details == rota:
                self.rotalar.remove(r)
                break

    def konaklama_sil(self, konaklama):
        for k in self.konaklamalar:
            if k.name == konaklama:
                self.konaklamalar.remove(k)
                break

class SeyahatPlanlamaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seyahat Planlama Uygulaması")
        self.setGeometry(100, 100, 600, 600)

        self.seyahat = Seyahat()

        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()

        self.page1_layout = QVBoxLayout()
        self.page1_layout.setAlignment(Qt.AlignTop)

        self.rota_label = QLabel("Rota Detayları:")
        self.rota_input = QComboBox()
        self.rota_input.addItems(["Turistik", "Ziyaret", "Eğlence", "Eğitim", "Spor"])

        self.seyahat_suresi_label = QLabel("Seyahat Süresi (Gün):")
        self.seyahat_suresi_input = QSpinBox()
        self.seyahat_suresi_input.setMinimum(1)
        self.seyahat_suresi_input.setMaximum(365)

        self.rota_ekle_button = QPushButton("Rota Ekle")
        self.rota_ekle_button.clicked.connect(self.rota_ekle)

        self.page1_layout.addWidget(self.rota_label)
        self.page1_layout.addWidget(self.rota_input)
        self.page1_layout.addWidget(self.seyahat_suresi_label)
        self.page1_layout.addWidget(self.seyahat_suresi_input)
        self.page1_layout.addWidget(self.rota_ekle_button)

        self.page1 = QWidget()
        self.page1.setLayout(self.page1_layout)
        self.stacked_widget.addWidget(self.page1)

        self.page2_layout = QVBoxLayout()
        self.page2_layout.setAlignment(Qt.AlignTop)

        self.konaklama_label = QLabel("Konaklama Yeri:")
        self.konaklama_input = QComboBox()
        self.konaklama_input.addItems(["Umay Otel", "Tomris Otel", "Kaan Pansiyon", "Göktuğ Otel"])
        self.konaklama_input.setEditable(True)
        self.konaklama_fiyat_label = QLabel("Fiyat Aralığı:")
        self.konaklama_fiyat_slider = QSlider(Qt.Horizontal)
        self.konaklama_fiyat_slider.setMinimum(0)
        self.konaklama_fiyat_slider.setMaximum(500)
        self.konaklama_fiyat_slider.setTickPosition(QSlider.TicksBelow)
        self.konaklama_fiyat_slider.setTickInterval(25)

        self.konaklama_ekle_button = QPushButton("Konaklama Ekle")
        self.konaklama_ekle_button.clicked.connect(self.konaklama_ekle)

        self.page2_layout.addWidget(self.konaklama_label)
        self.page2_layout.addWidget(self.konaklama_input)
        self.page2_layout.addWidget(self.konaklama_fiyat_label)
        self.page2_layout.addWidget(self.konaklama_fiyat_slider)
        self.page2_layout.addWidget(self.konaklama_ekle_button)

        self.page2 = QWidget()
        self.page2.setLayout(self.page2_layout)
        self.stacked_widget.addWidget(self.page2)

        self.page3_layout = QVBoxLayout()
        self.page3_layout.setAlignment(Qt.AlignTop)

        self.not_label = QLabel("Not Ekle:")
        self.not_input = QLineEdit()
        self.not_ekle_button = QPushButton("Not Ekle")
        self.not_ekle_button.clicked.connect(self.not_ekle)

        self.page3_layout.addWidget(self.not_label)
        self.page3_layout.addWidget(self.not_input)
        self.page3_layout.addWidget(self.not_ekle_button)

        self.page3 = QWidget()
        self.page3.setLayout(self.page3_layout)
        self.stacked_widget.addWidget(self.page3)

        self.page4_layout = QVBoxLayout()
        self.page4_layout.setAlignment(Qt.AlignTop)

        self.rota_table = QTableWidget()
        self.rota_table.setColumnCount(3)
        self.rota_table.setHorizontalHeaderLabels(["Rota Detayları", "Seyahat Süresi", "Notlar"])
        self.rota_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.konaklama_table = QTableWidget()
        self.konaklama_table.setColumnCount(3)
        self.konaklama_table.setHorizontalHeaderLabels(["Konaklama Yeri", "Fiyat", "Notlar"])
        self.konaklama_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.page4_layout.addWidget(self.rota_table)
        self.page4_layout.addWidget(self.konaklama_table)

        self.page4 = QWidget()
        self.page4.setLayout(self.page4_layout)
        self.stacked_widget.addWidget(self.page4)

        self.navigation_layout = QHBoxLayout()

        self.prev_button = QPushButton("<< Önceki")
        self.prev_button.clicked.connect(self.prev_page)

        self.next_button = QPushButton("Sonraki >>")
        self.next_button.clicked.connect(self.next_page)

        self.navigation_layout.addWidget(self.prev_button)
        self.navigation_layout.addWidget(self.next_button)

        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addLayout(self.navigation_layout)

        self.setLayout(self.main_layout)

        self.update_rota_table()
        self.update_konaklama_table()

    def prev_page(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)

    def next_page(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(current_index + 1)

    def rota_ekle(self):
        details = self.rota_input.currentText()
        seyahat_suresi = self.seyahat_suresi_input.value()
        if details:
            rota = Rota(details, seyahat_suresi)
            self.seyahat.rota_ekle(rota)
            self.rota_input.clear()
            self.update_rota_table()
        else:
            QMessageBox.warning(self, "Hata", "Rota detayları boş olamaz.")

    def konaklama_ekle(self):
        name = self.konaklama_input.currentText()
        price = self.konaklama_fiyat_slider.value()

        if name and price:
            konaklama = Konaklama(name, price)
            self.seyahat.konaklama_ekle(konaklama)
            self.update_konaklama_table()
        else:
            QMessageBox.warning(self, "Hata", "Konaklama yeri adı ve fiyatı boş olamaz.")

    def not_ekle(self):
        note_text = self.not_input.text()
        selected_table = self.rota_table if self.rota_input.hasFocus() else self.konaklama_table
        selected_row = selected_table.currentRow()
        if selected_row >= 0:
            selected_item = selected_table.item(selected_row, 0)
            if selected_item:
                item_text = selected_item.text()
                for rota in self.seyahat.rotalar:
                    if rota.details == item_text:
                        rota.add_note(note_text)
                        self.update_rota_table()
                        self.not_input.clear()
                        return
                for konaklama in self.seyahat.konaklamalar:
                    if konaklama.name == item_text:
                        konaklama.add_note(note_text)
                        self.update_konaklama_table()
                        self.not_input.clear()
                        return
        QMessageBox.warning(self, "Hata", "Önce bir rota veya konaklama yeri seçin.")

    def update_rota_table(self):
        self.rota_table.clearContents()
        self.rota_table.setRowCount(len(self.seyahat.rotalar))
        for i, rota in enumerate(self.seyahat.rotalar):
            self.rota_table.setItem(i, 0, QTableWidgetItem(rota.details))
            self.rota_table.setItem(i, 1, QTableWidgetItem(str(rota.seyahat_suresi)))
            self.rota_table.setItem(i, 2, QTableWidgetItem("\n".join(rota.notes)))

    def update_konaklama_table(self):
        self.konaklama_table.clearContents()
        self.konaklama_table.setRowCount(len(self.seyahat.konaklamalar))
        for i, konaklama in enumerate(self.seyahat.konaklamalar):
            self.konaklama_table.setItem(i, 0, QTableWidgetItem(konaklama.name))
            self.konaklama_table.setItem(i, 1, QTableWidgetItem(str(konaklama.price)))
            self.konaklama_table.setItem(i, 2, QTableWidgetItem("\n".join(konaklama.notes)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SeyahatPlanlamaApp()
    window.show()
    sys.exit(app.exec_())
