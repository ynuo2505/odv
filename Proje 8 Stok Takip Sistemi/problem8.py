from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QSpinBox, QComboBox, QDialog, QHBoxLayout
from PyQt5.QtCore import QDateTime, pyqtSignal  # Import pyqtSignal

class Product:
    def __init__(self, name, stock):
        self.name = name
        self.stock = stock
    
    def add_stock(self, quantity):
        self.stock += quantity
    
    def remove_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        else:
            return False

class Stock:
    def __init__(self):
        self.products = {}
    
    def add_product(self, product):
        self.products[product.name] = product
    
    def update_stock(self, product_name, quantity):
        if product_name in self.products:
            self.products[product_name].add_stock(quantity)
        else:
            print("Ürün bulunamadı.")
    
    def get_stock(self, product_name):
        if product_name in self.products:
            return self.products[product_name].stock
        else:
            return 0

    def get_all_products(self):
        return list(self.products.keys())

class Order:
    def __init__(self, product_name, quantity):
        self.product_name = product_name
        self.quantity = quantity
        self.timestamp = QDateTime.currentDateTime()  # Add timestamp when order is created
    
    def get_product_name(self):
        return self.product_name
    
    def get_quantity(self):
        return self.quantity

    def get_timestamp(self):
        return self.timestamp

class Orders:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def get_all_orders(self):
        return self.orders

class StockTrackingApp(QWidget):
    def __init__(self, stock):
        super().__init__()
        self.setWindowTitle("Stok Takip Sistemi")
        self.resize(600, 400)  # Resizing the main window
        
        self.layout = QVBoxLayout()
        self.setStyleSheet("background-color: #333; color: #fff;")  # Set background and text color of main window

        self.product_label = QLabel("Ürün:")
        self.product_label.setStyleSheet("font-size: 14px;")  # Styling label
        self.layout.addWidget(self.product_label)
        self.product_input = QLineEdit()
        self.layout.addWidget(self.product_input)

        self.quantity_label = QLabel("Miktar:")
        self.quantity_label.setStyleSheet("font-size: 14px;")  # Styling label
        self.layout.addWidget(self.quantity_label)
        self.quantity_input = QSpinBox()  # Changed to a spin box for selecting quantity
        self.quantity_input.setMinimum(1)  # Set minimum value
        self.quantity_input.setMaximum(9999)  # Set maximum value
        self.layout.addWidget(self.quantity_input)

        self.add_product_button = QPushButton("Ürün Ekle")
        self.add_product_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; margin: 4px 2px; cursor: pointer; border-radius: 5px;")  # Styling button
        self.add_product_button.clicked.connect(self.add_product)
        self.layout.addWidget(self.add_product_button)

        self.show_stock_button = QPushButton("Stokları Görüntüle")
        self.show_stock_button.setStyleSheet("background-color: #008CBA; color: white; font-size: 16px; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; margin: 4px 2px; cursor: pointer; border-radius: 5px;")  # Styling button
        self.show_stock_button.clicked.connect(self.show_stock)
        self.layout.addWidget(self.show_stock_button)

        self.show_order_window_button = QPushButton("Sipariş Ver")
        self.show_order_window_button.setStyleSheet("background-color: #f44336; color: white; font-size: 16px; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; margin: 4px 2px; cursor: pointer; border-radius: 5px;")  # Styling button
        self.show_order_window_button.clicked.connect(self.show_order_window)
        self.layout.addWidget(self.show_order_window_button)

        self.show_orders_button = QPushButton("Tüm Siparişleri Görüntüle")  # New button
        self.show_orders_button.setStyleSheet("background-color: #555; color: white; font-size: 16px; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; margin: 4px 2px; cursor: pointer; border-radius: 5px;")  # Styling button
        self.show_orders_button.clicked.connect(self.show_all_orders)  # Connect to slot
        self.layout.addWidget(self.show_orders_button)

        self.setLayout(self.layout)
        
        self.stock = stock
        self.stock_table = None
        self.orders = Orders()

    def add_product(self):
        product_name = self.product_input.text()
        quantity = self.quantity_input.value()  # Get selected quantity from spin box
        if not product_name:
            QMessageBox.warning(self, "Uyarı", "Ürün adı girmelisiniz.")
            return

        if product_name not in self.stock.products:
            self.stock.add_product(Product(product_name, quantity))  # Update: Initialize with quantity
            QMessageBox.information(self, "Bilgi", f"{product_name} ürünü eklendi.")
        else:
            QMessageBox.warning(self, "Uyarı", "Bu ürün zaten var.")
        
        self.product_input.clear()

    def show_stock(self):
        stock_list = self.stock.get_all_products()
        if not stock_list:
            QMessageBox.information(self, "Stoklar", "Stokta ürün bulunmamaktadır.")
        else:
            if not self.stock_table:
                self.stock_table = QTableWidget()
                self.stock_table.setStyleSheet("background-color: #f2f2f2; color: #333; font-size: 14px;")  # Styling table
                self.stock_table.setRowCount(len(stock_list))
                self.stock_table.setColumnCount(2)
                self.stock_table.setHorizontalHeaderLabels(["Ürün Adı", "Miktar"])

                for index, product_name in enumerate(stock_list):
                    self.stock_table.setItem(index, 0, QTableWidgetItem(product_name))
                    self.stock_table.setItem(index, 1, QTableWidgetItem(str(self.stock.get_stock(product_name))))

                self.stock_table.setWindowTitle("Stoklar")
                self.stock_table.show()
            else:
                self.stock_table.close()
                self.stock_table = None

    def show_order_window(self):
        order_window = OrderWindow(self.orders, self.stock, parent=self)
        order_window.order_placed.connect(self.refresh_orders)  # Connect signal to slot
        order_window.exec_()

    def show_all_orders(self):  # Slot to show all orders
        if not self.orders.get_all_orders():
            QMessageBox.information(self, "Siparişler", "Henüz sipariş yok.")
        else:
            if not self.stock_table:
                self.stock_table = QTableWidget()
                self.stock_table.setStyleSheet("background-color: #f2f2f2; color: #333; font-size: 14px;")  # Styling table
                self.stock_table.setColumnCount(3)
                self.stock_table.setHorizontalHeaderLabels(["Ürün Adı", "Miktar", "Eklenme Tarihi"])  # Add timestamp column

                orders = self.orders.get_all_orders()
                self.stock_table.setRowCount(len(orders))

                for index, order in enumerate(orders):
                    product_name = order.get_product_name()
                    quantity = order.get_quantity()
                    timestamp = order.get_timestamp().toString("yyyy-MM-dd HH:mm:ss")  # Convert timestamp to string
                    self.stock_table.setItem(index, 0, QTableWidgetItem(product_name))
                    self.stock_table.setItem(index, 1, QTableWidgetItem(str(quantity)))
                    self.stock_table.setItem(index, 2, QTableWidgetItem(timestamp))

                self.stock_table.setWindowTitle("Tüm Siparişler")
                self.stock_table.show()
            else:
                self.stock_table.close()
                self.stock_table = None

    def refresh_orders(self):
        if self.stock_table:
            self.show_stock()

class OrderWindow(QDialog):
    order_placed = pyqtSignal()  # Define a new signal

    def __init__(self, orders, stock, show_only=False, parent=None):  # Add parent parameter
        super().__init__(parent)
        self.setWindowTitle("Sipariş Görüntüleme Arayüzü")
        self.resize(300, 200)
        self.setStyleSheet("background-color: #333; color: #fff;")  # Set background and text color of dialog window

        self.layout = QVBoxLayout()

        self.orders = orders
        self.stock = stock

        if not show_only:
            self.product_label = QLabel("Ürün:")
            self.product_label.setStyleSheet("font-size: 14px;")  # Styling label
            self.layout.addWidget(self.product_label)
            self.product_combobox = QComboBox()
            self.product_combobox.addItems(stock.get_all_products())
            self.product_combobox.currentIndexChanged.connect(self.update_quantity_max)
            self.layout.addWidget(self.product_combobox)

            self.quantity_label = QLabel("Miktar:")
            self.quantity_label.setStyleSheet("font-size: 14px;")  # Styling label
            self.layout.addWidget(self.quantity_label)
            self.quantity_input = QSpinBox()  # Changed to a spin box for selecting quantity
            self.layout.addWidget(self.quantity_input)

            self.add_button = QPushButton("Sipariş Ekle")
            self.add_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; margin: 4px 2px; cursor: pointer; border-radius: 5px;")  # Styling button
            self.add_button.clicked.connect(self.add_order)
            self.layout.addWidget(self.add_button)

        self.orders_table = QTableWidget()
        self.orders_table.setStyleSheet("background-color: #f2f2f2; color: #333; font-size: 14px;")  # Styling table
        self.orders_table.setColumnCount(3)
        self.orders_table.setHorizontalHeaderLabels(["Ürün Adı", "Miktar", "Eklenme Tarihi"])  # Add timestamp column

        if not show_only:
            self.populate_orders_table()

        self.layout.addWidget(self.orders_table)
        self.setLayout(self.layout)

    def populate_orders_table(self):
        for index, order in enumerate(self.orders.get_all_orders()):
            product_name = order.get_product_name()
            quantity = order.get_quantity()
            timestamp = order.get_timestamp().toString("yyyy-MM-dd HH:mm:ss")  # Convert timestamp to string
            self.orders_table.insertRow(index)
            self.orders_table.setItem(index, 0, QTableWidgetItem(product_name))
            self.orders_table.setItem(index, 1, QTableWidgetItem(str(quantity)))
            self.orders_table.setItem(index, 2, QTableWidgetItem(timestamp))

    def update_quantity_max(self):
        selected_product = self.product_combobox.currentText()
        max_quantity = self.stock.get_stock(selected_product)
        self.quantity_input.setMaximum(max_quantity)  # Set maximum value equal to available stock

    def add_order(self):
        product_name = self.product_combobox.currentText()
        quantity = self.quantity_input.value()

        if not product_name:
            QMessageBox.warning(self, "Uyarı", "Ürün seçmelisiniz.")
            return

        if product_name not in self.stock.products:
            QMessageBox.warning(self, "Uyarı", "Geçerli bir ürün seçmelisiniz.")
            return

        if quantity <= 0:
            QMessageBox.warning(self, "Uyarı", "Geçerli bir miktar girmelisiniz.")
            return

        if quantity > self.stock.get_stock(product_name):
            QMessageBox.warning(self, "Uyarı", "Stok miktarından fazla sipariş veremezsiniz.")
            return

        order = Order(product_name, quantity)
        self.orders.add_order(order)
        QMessageBox.information(self, "Bilgi", f"{quantity} adet {product_name} sipariş oluşturuldu.")
        self.populate_orders_table()  # Update orders table
        self.order_placed.emit()  # Emit signal

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    stock = Stock()
    main_window = StockTrackingApp(stock)
    main_window.show()
    sys.exit(app.exec_())
