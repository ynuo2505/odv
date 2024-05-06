import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QInputDialog, QListWidgetItem, QSizePolicy, QDialog, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal, QObject, Qt

class StockUpdater(QObject):
    stock_updated = pyqtSignal()

class RestaurantInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Restaurant Interface")
        self.setGeometry(100, 100, 800, 600)  # Increased size
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.menu_items = {"Pizza": {"price": 10, "stock": 20}, "Burger": {"price": 8, "stock": 20}, "Salad": {"price": 6, "stock": 20}}
        self.orders = []
        self.stock_updater = StockUpdater()
        self.stock_updater.stock_updated.connect(self.update_menu_list)
        
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.menu_label = QLabel("Menu:")
        self.menu_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #eee;")
        self.layout.addWidget(self.menu_label)
        
        self.menu_list = QListWidget()
        self.menu_list.setStyleSheet("QListWidget { background-color: #333; color: #eee; border: none; padding: 10px; }"
                                      "QListWidget::item { background-color: #444; border: 1px solid #555; padding: 10px; }"
                                      "QListWidget::item:selected { background-color: #555; }")
        self.menu_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  
        self.populate_menu_list()
        self.menu_list.itemClicked.connect(self.show_item_stock)
        self.layout.addWidget(self.menu_list)
        
        self.order_label = QLabel("Order:")
        self.order_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #eee;")
        self.layout.addWidget(self.order_label)
        
        self.order_list = QListWidget()
        self.order_list.setStyleSheet("QListWidget { background-color: #333; color: #eee; border: none; padding: 10px; }"
                                       "QListWidget::item { background-color: #444; border: 1px solid #555; padding: 10px; }"
                                       "QListWidget::item:selected { background-color: #555; }")
        self.layout.addWidget(self.order_list)
        
        self.add_item_button = QPushButton("Add Item")
        self.add_item_button.setStyleSheet("font-size: 14px; font-weight: bold; color: #fff; background-color: #4CAF50; border: none; padding: 10px 20px; border-radius: 5px;")
        self.add_item_button.clicked.connect(self.add_item)
        self.layout.addWidget(self.add_item_button)
        
        self.remove_item_button = QPushButton("Remove Item")
        self.remove_item_button.setStyleSheet("font-size: 14px; font-weight: bold; color: #fff; background-color: #f44336; border: none; padding: 10px 20px; border-radius: 5px;")
        self.remove_item_button.clicked.connect(self.remove_item)
        self.layout.addWidget(self.remove_item_button)
        
        self.submit_order_button = QPushButton("Submit Order")
        self.submit_order_button.setStyleSheet("font-size: 16px; font-weight: bold; color: #fff; background-color: #2196F3; border: none; padding: 12px 24px; border-radius: 5px;")
        self.submit_order_button.clicked.connect(self.open_checkout_interface)
        self.layout.addWidget(self.submit_order_button)

        self.update_items_button = QPushButton("Update Items")
        self.update_items_button.setStyleSheet("font-size: 16px; font-weight: bold; color: #fff; background-color: #FF9800; border: none; padding: 12px 24px; border-radius: 5px;")
        self.update_items_button.clicked.connect(self.open_update_items_interface)
        self.layout.addWidget(self.update_items_button)
        
        self.order_history_button = QPushButton("Order History")  # Added Order History button
        self.order_history_button.setStyleSheet("font-size: 16px; font-weight: bold; color: #fff; background-color: #673AB7; border: none; padding: 12px 24px; border-radius: 5px;")
        self.order_history_button.clicked.connect(self.open_order_history_interface)  # Connect to open order history interface
        self.layout.addWidget(self.order_history_button)
        
        self.central_widget.setLayout(self.layout)

    def populate_menu_list(self):
        self.menu_list.clear()
        for item_name, details in self.menu_items.items():
            stock = details["stock"]
            item = QListWidgetItem(f"{item_name} - ${details['price']} (Stock: {stock})")
            item.setFlags(item.flags() |  Qt.ItemIsSelectable | Qt.ItemIsUserCheckable)
            self.menu_list.addItem(item)

    def show_item_stock(self, item):
        pass

    def add_item(self):
        selected_item = self.menu_list.currentItem()
        if selected_item:
            item_name = selected_item.text().split(' - ')[0]
            stock = self.menu_items[item_name]["stock"]
            if stock > 0:
                quantity, ok = QInputDialog.getInt(self, "Quantity", f"Enter quantity for {item_name}:")
                if ok:
                    if quantity <= stock:
                        # Check if the item is already in the order list
                        if not any(item.text().startswith(item_name) for item in self.order_list.findItems(item_name, Qt.MatchStartsWith)):
                            self.order_list.addItem(f"{item_name} - {quantity}")
                            self.menu_items[item_name]["stock"] -= quantity
                            self.populate_menu_list()
                        else:
                            QMessageBox.warning(self, "Duplicate Item", "You've already added this item to the order.")
                    else:
                        QMessageBox.warning(self, "Out of Stock", "Not enough stock available.")
            else:
                QMessageBox.warning(self, "Out of Stock", "This item is out of stock.")

    def remove_item(self):
        selected_item = self.order_list.currentItem()
        if selected_item:
            item_info = selected_item.text().split(' - ')
            item_name = item_info[0]
            quantity = int(item_info[1])
            self.order_list.takeItem(self.order_list.row(selected_item))
            self.menu_items[item_name]["stock"] += quantity
            self.populate_menu_list()

    def open_checkout_interface(self):
        checkout_window = CheckoutInterface(self.menu_items, self.order_list, self.orders)
        checkout_window.exec_()  # Use exec_() to open as a modal dialog

    def open_update_items_interface(self):
        self.update_items_window = UpdateItemsInterface(self.menu_items, self.stock_updater)
        self.update_items_window.show()

    def open_order_history_interface(self):  # Open order history interface
        order_history_window = OrderHistoryInterface(self.orders, self.menu_items)
        order_history_window.exec_()

    def update_menu_list(self):
        self.populate_menu_list()

class UpdateItemsInterface(QMainWindow):
    def __init__(self, menu_items, stock_updater):
        super().__init__()
        self.setWindowTitle("Update Items Interface")
        self.setGeometry(200, 200, 400, 300)
        self.menu_items = menu_items
        self.stock_updater = stock_updater
        
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.item_list_label = QLabel("Items:")
        self.layout.addWidget(self.item_list_label)

        self.item_list_widget = QListWidget()
        self.item_list_widget.setStyleSheet("QListWidget { background-color: #333; color: #eee; border: none; padding: 10px; }"
                                      "QListWidget::item { background-color: #444; border: 1px solid #555; padding: 10px; }"
                                      "QListWidget::item:selected { background-color: #555; }")
        self.item_list_widget.addItems(self.menu_items.keys())
        self.layout.addWidget(self.item_list_widget)

        self.price_label = QLabel("Price:")
        self.layout.addWidget(self.price_label)

        self.price_edit = QLineEdit()
        self.layout.addWidget(self.price_edit)

        self.stock_label = QLabel("Stock:")
        self.layout.addWidget(self.stock_label)

        self.stock_edit = QLineEdit()
        self.layout.addWidget(self.stock_edit)

        self.add_new_item_layout = QHBoxLayout()
        self.new_item_name_label = QLabel("New Item Name:")
        self.add_new_item_layout.addWidget(self.new_item_name_label)
        self.new_item_name_edit = QLineEdit()
        self.add_new_item_layout.addWidget(self.new_item_name_edit)
        self.layout.addLayout(self.add_new_item_layout)

        self.add_new_item_button = QPushButton("Add New Item")
        self.add_new_item_button.setStyleSheet("font-size: 14px; font-weight: bold; color: #fff; background-color: #4CAF50; border: none; padding: 10px 20px; border-radius: 5px;")
        self.add_new_item_button.clicked.connect(self.add_new_item)
        self.layout.addWidget(self.add_new_item_button)

        self.update_button = QPushButton("Update")
        self.update_button.setStyleSheet("font-size: 14px; font-weight: bold; color: #fff; background-color: #FF9800; border: none; padding: 10px 20px; border-radius: 5px;")
        self.update_button.clicked.connect(self.update_item)
        self.layout.addWidget(self.update_button)

        self.central_widget.setLayout(self.layout)

        self.item_list_widget.itemClicked.connect(self.show_item_details)

    def show_item_details(self, item):
        item_name = item.text()
        self.price_edit.setText(str(self.menu_items[item_name]["price"]))
        self.stock_edit.setText(str(self.menu_items[item_name]["stock"]))

    def update_item(self):
        selected_item = self.item_list_widget.currentItem()
        if selected_item:
            item_name = selected_item.text()
            price = self.price_edit.text()
            stock = self.stock_edit.text()
            try:
                price = float(price)
                stock = int(stock)
                if stock > 9999:
                    QMessageBox.warning(self, "Invalid Stock", "Maximum stock allowed is 9999.")
                else:
                    self.menu_items[item_name]["price"] = price
                    self.menu_items[item_name]["stock"] = stock
                    QMessageBox.information(self, "Success", "Item updated successfully.")
                    self.stock_updater.stock_updated.emit()
            except ValueError:
                QMessageBox.warning(self, "Error", "Please enter valid price and stock values.")
        else:
            QMessageBox.warning(self, "Error", "Please select an item to update.")

    def add_new_item(self):
        new_item_name = self.new_item_name_edit.text()
        if new_item_name and new_item_name not in self.menu_items:
            price = self.price_edit.text()
            stock = self.stock_edit.text()
            try:
                price = float(price)
                stock = int(stock)
                if stock > 9999:
                    QMessageBox.warning(self, "Invalid Stock", "Maximum stock allowed is 9999.")
                else:
                    self.menu_items[new_item_name] = {"price": price, "stock": stock}
                    self.item_list_widget.addItem(new_item_name)
                    QMessageBox.information(self, "Success", "New item added successfully.")
                    self.stock_updater.stock_updated.emit()
                    self.new_item_name_edit.clear()  
            except ValueError:
                QMessageBox.warning(self, "Error", "Please enter valid price and stock values.")

class CheckoutInterface(QDialog):  # Modified CheckoutInterface to display items and quantities
    def __init__(self, menu_items, order_list, orders):
        super().__init__()
        self.setWindowTitle("Checkout")
        self.setGeometry(200, 200, 600, 400)  # Increased size
        self.menu_items = menu_items
        self.order_list = order_list
        self.orders = orders
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        table_widget = QTableWidget()
        table_widget.setColumnCount(4)
        table_widget.setHorizontalHeaderLabels(["Item", "Quantity", "Price", "Total"])

        total_price = 0
        for i in range(self.order_list.count()):
            item_info = self.order_list.item(i).text().split(' - ')
            item_name = item_info[0]
            quantity = int(item_info[1])
            price = self.menu_items[item_name]["price"]
            total_price += price * quantity
            table_widget.insertRow(i)
            table_widget.setItem(i, 0, QTableWidgetItem(item_name))
            table_widget.setItem(i, 1, QTableWidgetItem(str(quantity)))
            table_widget.setItem(i, 2, QTableWidgetItem(f"${price}"))
            table_widget.setItem(i, 3, QTableWidgetItem(f"${price * quantity}"))

        layout.addWidget(table_widget)

        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setStyleSheet("color: white;")  # Adjusted text color
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        address_layout = QHBoxLayout()
        address_label = QLabel("Address:")
        address_label.setStyleSheet("color: white;")  # Adjusted text color
        self.address_edit = QLineEdit()
        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_edit)
        layout.addLayout(address_layout)

        summary_label = QLabel(f"Total Price: ${total_price}")
        layout.addWidget(summary_label)

        checkout_button = QPushButton("Checkout")
        checkout_button.clicked.connect(self.checkout)
        layout.addWidget(checkout_button)

        self.setLayout(layout)

    def checkout(self):
        order_number = random.randint(1000, 9999)
        name = self.name_edit.text()
        address = self.address_edit.text()
        self.orders.append({"Order Number": order_number, "Name": name, "Address": address, "Items": []})  # Append order to orders list
        for i in range(self.order_list.count()):
            item_info = self.order_list.item(i).text().split(' - ')
            item_name = item_info[0]
            quantity = int(item_info[1])
            self.orders[-1]["Items"].append({"Item": item_name, "Quantity": quantity})  # Append items to the last order in the list
        QMessageBox.information(self, "Order Placed", f"Order successfully placed!\nOrder Number: {order_number}\nName: {name}\nAddress: {address}")
        self.close()  # Close the dialog after checkout

class OrderHistoryInterface(QDialog):
    def __init__(self, orders, menu_items):
        super().__init__()
        self.setWindowTitle("Order History")
        self.setGeometry(200, 200, 800, 600)  # Increased size
        self.orders = orders
        self.menu_items = menu_items

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        table_widget = QTableWidget()
        table_widget.setColumnCount(6)
        table_widget.setHorizontalHeaderLabels(["Order Number", "Name", "Address", "Item", "Quantity", "Total Price"])

        row = 0
        for order in self.orders:
            total_price = 0
            for item in order["Items"]:
                item_name = item["Item"]
                quantity = item["Quantity"]
                price = self.menu_items[item_name]["price"]
                total_price += price * quantity
                table_widget.insertRow(row)
                table_widget.setItem(row, 0, QTableWidgetItem(str(order["Order Number"])))
                table_widget.setItem(row, 1, QTableWidgetItem(order["Name"]))
                table_widget.setItem(row, 2, QTableWidgetItem(order["Address"]))
                table_widget.setItem(row, 3, QTableWidgetItem(item_name))
                table_widget.setItem(row, 4, QTableWidgetItem(str(quantity)))
                table_widget.setItem(row, 5, QTableWidgetItem(f"${price * quantity}"))
                row += 1

            table_widget.insertRow(row)
            table_widget.setItem(row, 5, QTableWidgetItem(f"Total Price: ${total_price}"))
            row += 1

        layout.addWidget(table_widget)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #222; color: #eee; }"  # Set background and text color for all widgets
                      "QMainWindow { background-color: #222; }"  # Darker background color
                      "QLabel { color: #eee; }"  # Text color
                      "QLineEdit { background-color: #333; color: #eee; border: 1px solid #555; padding: 5px; }"  # LineEdit style
                      "QPushButton { font-size: 14px; font-weight: bold; color: #fff; background-color: #555; border: none; padding: 10px 20px; border-radius: 5px; }"  # Button style
                      "QPushButton:hover { background-color: #777; }"  # Hover effect for buttons
                      "QTableWidget { background-color: #333; color: #eee; border: none; }"  # TableWidget style
                      "QHeaderView::section { background-color: #444; color: #eee; border: none; padding: 5px; }"  # Table header style
                      "QHeaderView::section:hover { background-color: #555; }")  # Hover effect for table headers
    window = RestaurantInterface()
    window.show()
    sys.exit(app.exec_())