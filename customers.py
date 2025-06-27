from PyQt5 import QtWidgets, QtCore
import sqlite3

class CustomerManager(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مدیریت مشتری‌ها")
        self.setGeometry(250, 150, 700, 500)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.form = QtWidgets.QFormLayout()
        self.name_input = QtWidgets.QLineEdit()
        self.phone_input = QtWidgets.QLineEdit()
        self.email_input = QtWidgets.QLineEdit()
        self.address_input = QtWidgets.QLineEdit()

        self.form.addRow("نام:", self.name_input)
        self.form.addRow("تلفن:", self.phone_input)
        self.form.addRow("ایمیل:", self.email_input)
        self.form.addRow("آدرس:", self.address_input)

        self.layout.addLayout(self.form)

        self.add_button = QtWidgets.QPushButton("افزودن مشتری")
        self.add_button.clicked.connect(self.add_customer)
        self.layout.addWidget(self.add_button)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["کد", "نام", "تلفن", "ایمیل", "آدرس"])
        self.layout.addWidget(self.table)

        self.load_customers()

    def add_customer(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()

        conn = sqlite3.connect("samtronic.db")
        c = conn.cursor()
        c.execute("INSERT INTO customers (name, phone, email, address) VALUES (?, ?, ?, ?)",
                  (name, phone, email, address))
        conn.commit()
        conn.close()

        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.load_customers()

    def load_customers(self):
        self.table.setRowCount(0)
        conn = sqlite3.connect("samtronic.db")
        c = conn.cursor()
        c.execute("SELECT id, name, phone, email, address FROM customers")
        for row_index, row_data in enumerate(c.fetchall()):
            self.table.insertRow(row_index)
            for column, data in enumerate(row_data):
                self.table.setItem(row_index, column, QtWidgets.QTableWidgetItem(str(data)))
        conn.close()