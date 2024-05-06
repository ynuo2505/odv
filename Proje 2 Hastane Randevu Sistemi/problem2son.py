import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCalendarWidget, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QMessageBox, QLineEdit, QComboBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QDate

class Doktor:
    def __init__(self, isim, uzmanlik_alani):
        self.isim = isim
        self.uzmanlik_alani = uzmanlik_alani
        self.musaitlik_durumu = True

class Randevu:
    def __init__(self, tarih, saat, doktor, hasta_ad, hasta_soyad, hasta_tc):
        self.tarih = tarih
        self.saat = saat
        self.doktor = doktor
        self.hasta_ad = hasta_ad
        self.hasta_soyad = hasta_soyad
        self.hasta_tc = hasta_tc

class RandevuSistemiUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Randevu Sistemi")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.doctor_data = [
            Doktor("Berkay Öztürk", "Dahiliye"),
            Doktor("Uğurkan Köse", "Kulak Burun Boğaz"),
            Doktor("Edanur Muslukçu", "Göz Hastalıkları"),
            Doktor("Alperen Yunus Bulut", "Ortopedi"),
            
        ]
        self.appointments = []

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("background-color: white; color: black;")
        self.calendar.setGridVisible(True)
        self.calendar.selectionChanged.connect(self.update_appointment_table)
        layout.addWidget(self.calendar)

        self.hasta_ad_label = QLabel("Hasta Adı:")
        layout.addWidget(self.hasta_ad_label)
        self.hasta_ad_input = QLineEdit()
        layout.addWidget(self.hasta_ad_input)

        self.hasta_soyad_label = QLabel("Hasta Soyadı:")
        layout.addWidget(self.hasta_soyad_label)
        self.hasta_soyad_input = QLineEdit()
        layout.addWidget(self.hasta_soyad_input)

        self.hasta_tc_label = QLabel("Hasta TC:")
        layout.addWidget(self.hasta_tc_label)
        self.hasta_tc_input = QLineEdit()
        layout.addWidget(self.hasta_tc_input)

        self.doktor_combo = QComboBox()
        self.doktor_combo.addItems([doktor.isim for doktor in self.doctor_data])
        layout.addWidget(QLabel("Doktor Seç:"))
        layout.addWidget(self.doktor_combo)

        self.time_combo = QComboBox()
        self.time_combo.addItems(["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"])
        layout.addWidget(QLabel("Randevu Saati:"))
        layout.addWidget(self.time_combo)

        self.appointment_table = QTableWidget()
        self.appointment_table.setColumnCount(6)
        self.appointment_table.setHorizontalHeaderLabels(["Tarih", "Saat", "Doktor", "Hasta Adı", "Hasta Soyadı", "Hasta TC", "İptal"])
        layout.addWidget(QLabel("Randevular"))
        layout.addWidget(self.appointment_table)

        button_layout = QVBoxLayout()
        self.randevu_al_button = QPushButton("Randevu Al")
        self.randevu_al_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.randevu_al_button.clicked.connect(self.randevu_al)
        button_layout.addWidget(self.randevu_al_button)

        self.randevu_iptal_button = QPushButton("Randevu İptal")
        self.randevu_iptal_button.setStyleSheet("background-color: #f44336; color: white;")
        self.randevu_iptal_button.clicked.connect(self.cancel_appointment)
        button_layout.addWidget(self.randevu_iptal_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.show()

    def update_appointment_table(self):
        selected_date = self.calendar.selectedDate()
        filtered_appointments = [randevu for randevu in self.appointments if randevu.tarih == selected_date.toString("dd/MM/yyyy")]
        self.appointment_table.setRowCount(len(filtered_appointments))
        for i, randevu in enumerate(filtered_appointments):
            self.appointment_table.setItem(i, 0, QTableWidgetItem(randevu.tarih))
            self.appointment_table.setItem(i, 1, QTableWidgetItem(randevu.saat))
            self.appointment_table.setItem(i, 2, QTableWidgetItem(randevu.doktor))
            self.appointment_table.setItem(i, 3, QTableWidgetItem(randevu.hasta_ad))
            self.appointment_table.setItem(i, 4, QTableWidgetItem(randevu.hasta_soyad))
            self.appointment_table.setItem(i, 5, QTableWidgetItem(randevu.hasta_tc))
            cancel_button = QPushButton("İptal")
            cancel_button.setStyleSheet("background-color: #f44336; color: white;")
            cancel_button.clicked.connect(lambda _, row=i: self.cancel_appointment(row))
            self.appointment_table.setCellWidget(i, 6, cancel_button)

    def randevu_al(self):
        selected_date = self.calendar.selectedDate()
        doktor_index = self.doktor_combo.currentIndex()
        doktor = self.doctor_data[doktor_index]
        saat = self.time_combo.currentText()
        hasta_ad = self.hasta_ad_input.text()
        hasta_soyad = self.hasta_soyad_input.text()
        hasta_tc = self.hasta_tc_input.text()
        if len(hasta_tc) != 11:
            QMessageBox.warning(self, "Hata", "Hasta TC 11 karakter olmalıdır.")
            return
        if hasta_ad and hasta_soyad and hasta_tc:
            # Aynı saat ve doktora zaten başka bir randevu alınmış mı kontrol et
            for randevu in self.appointments:
                if randevu.tarih == selected_date.toString("dd/MM/yyyy") and randevu.saat == saat and randevu.doktor == doktor.isim:
                    QMessageBox.warning(self, "Hata", "Bu saatte ve doktorda zaten bir randevu var.")
                    return
            randevu = Randevu(selected_date.toString("dd/MM/yyyy"), saat, doktor.isim, hasta_ad, hasta_soyad, hasta_tc)
            self.appointments.append(randevu)
            self.update_appointment_table()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen hasta bilgilerini girin.")

    def cancel_appointment(self, row):
        confirmation = QMessageBox.question(self, "Randevu İptali", "Seçilen randevuyu iptal etmek istiyor musunuz?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            del self.appointments[row]
            self.update_appointment_table()
            QMessageBox.information(self, "İptal", "Randevu iptal edildi.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = RandevuSistemiUI()
    sys.exit(app.exec_())
