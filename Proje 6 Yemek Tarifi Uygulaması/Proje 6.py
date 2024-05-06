import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QGroupBox, QTextBrowser, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Yemek Tarifleri
yemek_tarifleri = {
    "Omlet": {
        "Malzemeler": ["Yumurta", "Süt", "Tuz", "Karabiber", "Peynir (isteğe bağlı)", "Yeşillikler (isteğe bağlı)"],
        "Tarif": """
            1. Yumurtaları bir kaseye kırın.
            2. Üzerine süt, tuz ve karabiber ekleyin, iyice çırpın.
            3. Bir tavada yağı ısıtın.
            4. Çırpılmış yumurta karışımını tavaya dökün.
            5. Altı pişmeye başlayınca, peynir ve yeşilliklerle üzerini süsleyin.
            6. Altı kızardığında, omleti katlayın ve servis yapın.
        """
    },
    "Mercimek Çorbası": {
        "Malzemeler": ["Kırmızı mercimek", "Soğan", "Havuç", "Domates", "Tuz", "Karabiber", "Zeytinyağı"],
        "Tarif": """
            1. Soğanı ve havucu doğrayın, bir tencerede zeytinyağında kavurun.
            2. Kırmızı mercimeği ekleyin, üzerine su ekleyin ve kaynamaya bırakın.
            3. Mercimekler yumuşayıncaya kadar pişirin.
            4. Domates ekleyin, tuz ve karabiberle tatlandırın.
            5. Blenderdan geçirin ve servis yapın.
        """
    },
    "Tavuklu Salata": {
        "Malzemeler": ["Tavuk göğsü", "Marul", "Domates", "Salatalık", "Zeytinyağı", "Limon suyu", "Tuz", "Karabiber"],
        "Tarif": """
            1. Tavuk göğsünü haşlayın, didikleyin.
            2. Marul, domates ve salatalığı doğrayın.
            3. Bir kasede tavuk göğsü ve doğranmış sebzeleri karıştırın.
            4. Üzerine zeytinyağı, limon suyu, tuz ve karabiber ekleyin.
            5. Karıştırın ve servis yapın.
        """
    }
}


class RecipeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yemek Tarifi Uygulaması")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icon.png'))

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }

            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
            }

            QPushButton:hover {
                background-color: #45a049;
            }

            QTextEdit, QLineEdit, QTextBrowser {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
            }

            QLabel {
                font-weight: bold;
                font-size: 16px;
            }
        """)

        self.username_label = QLabel("Kullanıcı Adı:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Giriş")

        self.recipe_list_label = QLabel("Yemek Tarifleri")
        self.recipe_list = QTextBrowser()
        self.recipe_list.anchorClicked.connect(self.display_recipe)

        self.recipe_edit_label = QLabel("Tarif Ekleyin veya Düzenleyin:")
        self.recipe_edit_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.recipe_edit_label.setStyleSheet("font-size: 18px; font-weight: bold; color: blue;")

        self.recipe_name_label = QLabel("Tarif Adı:")
        self.recipe_name_input = QLineEdit()
        self.ingredients_label = QLabel("Malzemeler:")
        self.ingredients_input = QTextEdit()
        self.instructions_label = QLabel("Tarif İçeriği:")
        self.instructions_input = QTextEdit()
        self.submit_button = QPushButton("Kaydet")
        self.refresh_button = QPushButton("Yenile")

        recipe_editor_groupbox = QGroupBox("Tarif Ekleyin veya Düzenleyin")
        recipe_editor_layout = QVBoxLayout()
        recipe_editor_layout.addWidget(self.recipe_name_label)
        recipe_editor_layout.addWidget(self.recipe_name_input)
        recipe_editor_layout.addWidget(self.ingredients_label)
        recipe_editor_layout.addWidget(self.ingredients_input)
        recipe_editor_layout.addWidget(self.instructions_label)
        recipe_editor_layout.addWidget(self.instructions_input)
        recipe_editor_layout.addWidget(self.submit_button)
        recipe_editor_layout.addWidget(self.refresh_button)
        recipe_editor_groupbox.setLayout(recipe_editor_layout)

        login_groupbox = QGroupBox()
        login_layout = QVBoxLayout()
        login_layout.addWidget(self.username_label)
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(self.password_label)
        login_layout.addWidget(self.password_input)
        login_layout.addWidget(self.login_button)
        login_groupbox.setLayout(login_layout)

        recipe_groupbox = QGroupBox("Tarifler")
        recipe_layout = QVBoxLayout()
        recipe_layout.addWidget(self.recipe_list_label)
        recipe_layout.addWidget(self.recipe_list)
        recipe_groupbox.setLayout(recipe_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(login_groupbox)
        main_layout.addWidget(recipe_groupbox)
        main_layout.addWidget(recipe_editor_groupbox)
        self.setLayout(main_layout)

        self.login_button.clicked.connect(self.check_credentials)
        self.submit_button.clicked.connect(self.save_or_update_recipe)
        self.refresh_button.clicked.connect(self.refresh_recipe)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            self.username_label.setParent(None)
            self.username_input.setParent(None)
            self.password_label.setParent(None)
            self.password_input.setParent(None)
            self.login_button.setParent(None)
            self.show_recipe_list()
        else:
            QMessageBox.critical(self, "Hata", "Geçersiz kullanıcı adı veya şifre.")

    def show_recipe_list(self):
        self.recipe_list.clear()
        for recipe_name in yemek_tarifleri.keys():
            self.recipe_list.append(f"<a href=\"{recipe_name}\">{recipe_name}</a>")

    def display_recipe(self, link):
        recipe_name = link.toString()
        recipe = yemek_tarifleri.get(recipe_name)
        if recipe:
            ingredients = ', '.join(recipe["Malzemeler"])
            instructions = recipe["Tarif"]
            self.recipe_name_input.setText(recipe_name)
            self.ingredients_input.setPlainText(ingredients)
            self.instructions_input.setPlainText(instructions)
        else:
            QMessageBox.warning(self, "Uyarı", "Tarif bulunamadı.")

    def save_or_update_recipe(self):
        recipe_name = self.recipe_name_input.text()
        ingredients = self.ingredients_input.toPlainText().split(', ')
        instructions = self.instructions_input.toPlainText()
        yemek_tarifleri[recipe_name] = {"Malzemeler": ingredients, "Tarif": instructions}
        QMessageBox.information(self, "Başarılı", "Tarif başarıyla kaydedildi.")
        self.show_recipe_list()

    def refresh_recipe(self):
        self.recipe_name_input.clear()
        self.ingredients_input.clear()
        self.instructions_input.clear()
        self.show_recipe_list()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecipeApp()
    window.show()
    sys.exit(app.exec_())
