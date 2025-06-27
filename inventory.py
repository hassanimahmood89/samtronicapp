from PyQt5 import QtWidgets
import sqlite3


class InventoryManager(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مدیریت انبار")
        self.setGeometry(300, 200, 750, 500)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        form = QtWidgets.QFormLayout()
        self.name_input = QtWidgets.QLineEdit()
        self.quantity_input = QtWidgets.QSpinBox()
        self.quantity_input.setMaximum(10000)
        self.buy_price_input = QtWidgets.QLineEdit()
        self.sell_price_input = QtWidgets.QLineEdit()

        form.addRow("نام قطعه:", self.name_input)
        form.addRow("تعداد:", self.quantity_input)
        form.addRow("قیمت خرید:", self.buy_price_input)
        form.addRow("قیمت فروش:", self.sell_price_input)
        self.layout.addLayout(form)

        self.add_btn = QtWidgets.QPushButton("➕ افزودن قطعه")
        self.add_btn.clicked.connect(self.add_part)
        self.layout.addWidget(self.add_btn)

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("🔍 جستجوی قطعه...")
        self.search_input.textChanged.connect(self.load_parts)
        self.layout.addWidget(self.search_input)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["نام", "تعداد", "خرید", "فروش"])
        self.layout.addWidget(self.table)

        self.load_parts()

    def add_part(self):
        name = self.name_input.text()
        quantity = self.quantity_input.value()
        buy_price = self.buy_price_input.text()
        sell_price = self.sell_price_input.text()

        conn = sqlite3.connect("samtronic.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO inventory (name, quantity, buy_price, sell_price) VALUES (?, ?, ?, ?)",
            (name, quantity, buy_price, sell_price),
        )
        conn.commit()
        conn.close()

        self.name_input.clear()
        self.quantity_input.setValue(0)
        self.buy_price_input.clear()
        self.sell_price_input.clear()
        self.load_parts()

    def load_parts(self):
        self.table.setRowCount(0)
        keyword = self.search_input.text().lower()
        conn = sqlite3.connect("samtronic.db")
        c = conn.cursor()
        c.execute("SELECT name, quantity, buy_price, sell_price FROM inventory")
        for row in c.fetchall():
            if keyword in row[0].lower():
                row_idx = self.table.rowCount()
                self.table.insertRow(row_idx)
                for col, val in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(val))
                    if col == 1 and int(val) < 5:
                        item.setBackground(QtWidgets.QColor("red"))
                    self.table.setItem(row_idx, col, item)
        conn.close()
