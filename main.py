import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTableWidget,
                               QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox)
from PySide6.QtCore import Qt, QSize
import sqlite3


# Создание базы данных и таблицы
def init_db():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  customer_name TEXT,
                  order_details TEXT,
                  status TEXT)''')
    conn.commit()
    conn.close()


# Функция для добавления заказа
def add_order(customer_name, order_details):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'New')",
              (customer_name, order_details))
    conn.commit()
    conn.close()


# Функция для просмотра заказов
def view_orders(table_widget):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    rows = c.fetchall()
    conn.close()

    table_widget.setRowCount(len(rows))
    table_widget.setColumnCount(4)
    table_widget.setHorizontalHeaderLabels(["ID", "Customer Name", "Order Details", "Status"])

    for row_index, row_data in enumerate(rows):
        for col_index, col_data in enumerate(row_data):
            table_widget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Order Management System")
        self.setFixedSize(QSize(600, 600))
        self.layout = QVBoxLayout()

        self.client_name_label = QLabel("Client name:")
        self.layout.addWidget(self.client_name_label)

        self.client_name_input = QLineEdit()
        self.layout.addWidget(self.client_name_input)

        self.order_details_label = QLabel("Order details:")
        self.layout.addWidget(self.order_details_label)

        self.order_details_input = QLineEdit()
        self.layout.addWidget(self.order_details_input)

        # Создание контейнера для кнопок
        self.button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Order")
        self.add_button.setFixedSize(150, 30)
        self.add_button.clicked.connect(self.on_add_button_clicked)
        self.button_layout.addWidget(self.add_button)

        self.complete_button = QPushButton("Complete Order")
        self.complete_button.setFixedSize(150, 30)
        self.complete_button.clicked.connect(self.on_complete_button_clicked)
        self.button_layout.addWidget(self.complete_button)

        self.layout.addLayout(self.button_layout)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.view_orders()

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def on_add_button_clicked(self):
        customer_name = self.client_name_input.text()
        order_details = self.order_details_input.text()
        if customer_name and order_details:
            add_order(customer_name, order_details)
            self.view_orders()
            self.client_name_input.clear()
            self.order_details_input.clear()

    def on_complete_button_clicked(self):
        selected_row = self.table_widget.currentRow()
        if selected_row != -1:
            status_item = self.table_widget.item(selected_row, 3)
            if status_item.text() != "Complete":
                order_id = int(self.table_widget.item(selected_row, 0).text())
                conn = sqlite3.connect('orders.db')
                c = conn.cursor()
                c.execute("UPDATE orders SET status = 'Complete' WHERE id = ?", (order_id,))
                conn.commit()
                conn.close()
                self.view_orders()
            else:
                QMessageBox.warning(self, "Warning", "The selected order is already completed.")
        else:
            QMessageBox.warning(self, "Warning", "No order selected.")

    def view_orders(self):
        view_orders(self.table_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    init_db()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
