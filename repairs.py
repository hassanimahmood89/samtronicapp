from PyQt5 import QtWidgets
import sqlite3


class RepairManager(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ثبت تعمیرات")
        self.setGeometry(300, 200, 950, 600)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        form = QtWidgets.QFormLayout()
        self.customer_combo = QtWidgets.QComboBox()
        self.device_input = QtWidgets.QLineEdit()
        self.problem_input = QtWidgets.QLineEdit()
        self.status_combo = QtWidgets.QComboBox()
        self.status_combo.addItems(
            ["در انتظار قطعه", "در حال تعمیر", "آماده تحویل", "تحویل‌شده"]
        )
        self.cost_input = QtWidgets.QLineEdit()
        self.note_input = QtWidgets.QLineEdit()
        self.warranty_input = QtWidgets.QLineEdit()

        self.part_combo = QtWidgets.QComboBox()
        self.quantity_input = QtWidgets.QSpinBox()
        self.quantity_input.setMaximum(1000)
        add_part_btn = QtWidgets.QPushButton("➕ افزودن قطعه")
        add_part_btn.clicked.connect(self.add_part_to_list)

        form.addRow("مشتری:", self.customer_combo)
        form.addRow("دستگاه:", self.device_input)
        form.addRow("مشکل:", self.problem_input)
        form.addRow("وضعیت:", self.status_combo)
        form.addRow("هزینه:", self.cost_input)
        form.addRow("یادداشت:", self.note_input)
        form.addRow("گارانتی:", self.warranty_input)
        form.addRow("قطعه:", self.part_combo)
        form.addRow("تعداد:", self.quantity_input)
        form.addRow("", add_part_btn)
        self.layout.addLayout(form)

        self.parts_table = QtWidgets.QTableWidget()
        self.parts_table.setColumnCount(3)
        self.parts_table.setHorizontalHeaderLabels(["نام قطعه", "ID", "تعداد"])
        self.layout.addWidget(self.parts_table)

        self.save_btn = QtWidgets.QPushButton("💾 ثبت تعمیر")
        self.save_btn.clicked.connect(self.save_repair)
        self.layout.addWidget(self.save_btn)

        search_layout = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("🔍 جستجو...")
        self.search_input.textChanged.connect(self.load_repairs)
        search_layout.addWidget(self.search_input)
        self.layout.addLayout(search_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "مشتری", "دستگاه", "مشکل", "هزینه", "قطعات", "وضعیت"]
        )
        self.table.cellDoubleClicked.connect(self.generate_invoice)
        self.layout.addWidget(self.table)

        self.parts_used = []
        self.load_customers()
        self.load_parts()
        self.load_repairs()

    def load_customers(self):
        conn = sqlite3.connect("samtronic.db")
        c = conn.cursor()
        c.execute("SELECT id, name FROM customers")
        self.customer_combo.clear()
        for customer in c.fetchall():
            self.customer_combo.addItem(customer[1], customer[0])
        conn.close()

    def load_parts(self):
        conn = sqlite3.connect("samtronic.db")
        c = conn.cursor()
        c.execute("SELECT id, name, quantity FROM inventory")
        self.parts = c.fetchall()
        self.part_combo.clear()
        for part in self.parts:
            alert = "⚠️" if part[2] < 5 else ""
            self.part_combo.addItem(f"{part[1]} ({part[2]}) {alert}", part[0])
        conn.close()

    def add_part_to_list(self):
        part_id = self.part_combo.currentData()
        quantity = self.quantity_input.value()
        if quantity <= 0:
            QtWidgets.QMessageBox.warning(self, "خطا", "تعداد باید بیشتر از صفر باشد.")
            return
        for part in self.parts:
            if part[0] == part_id:
                if quantity > part[2]:
                    QtWidgets.QMessageBox.warning(
                        self, "موجودی ناکافی", f"تنها {part[2]} عدد موجود است."
                    )
                    return
                self.parts_used.append((part_id, part[1], quantity))
                break
        self.refresh_parts_table()

    def refresh_parts_table(self):
        self.parts_table.setRowCount(0)
        for i, (part_id, name, qty) in enumerate(self.parts_used):
            self.parts_table.insertRow(i)
            self.parts_table.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            self.parts_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(part_id)))
            self.parts_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(qty)))

    def save_repair(self):
        customer_id = self.customer_combo.currentData()
        device = self.device_input.text()
        problem = self.problem_input.text()
        status = self.status_combo.currentText()
        cost = self.cost_input.text()
        note = self.note_input.text()
        warranty = self.warranty_input.text()

        if not self.parts_used:
            QtWidgets.QMessageBox.warning(self, "خطا", "هیچ قطعه‌ای انتخاب نشده.")
            return

        conn = sqlite3.connect("samtronic.db")
        c = conn.cursor()
        c.execute(
            """INSERT INTO repairs (customer_id, device, problem, status, cost, note, warranty)
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (customer_id, device, problem, status, cost, note, warranty),
        )
        repair_id = c.lastrowid

        for part_id, _, qty in self.parts_used:
            c.execute(
                "INSERT INTO repair_parts (repair_id, part_id, quantity_used) VALUES (?, ?, ?)",
                (repair_id, part_id, qty),
            )
            c.execute(
                "UPDATE inventory SET quantity = quantity - ? WHERE id = ?",
                (qty, part_id),
            )

        conn.commit()
        conn.close()
        self.device_input.clear()
        self.problem_input.clear()
        self.cost_input.clear()
        self.note_input.clear()
        self.warranty_input.clear()
        self.parts_used.clear()
        self.refresh_parts_table()
        self.load_parts()
        self.load_repairs()

    def load_repairs(self):
        keyword = self.search_input.text().lower()
        self.table.setRowCount(0)
        conn = sqlite3.connect("samtronic.db")
        c = conn.cursor()
        c.execute(
            """SELECT r.id, c.name, r.device, r.problem, r.cost, r.status
                     FROM repairs r
                     JOIN customers c ON r.customer_id = c.id"""
        )
        all_repairs = c.fetchall()

        for row in all_repairs:
            if keyword in " ".join(str(cell).lower() for cell in row):
                repair_id = row[0]
                c.execute(
                    """SELECT i.name, rp.quantity_used FROM repair_parts rp
                             JOIN inventory i ON rp.part_id = i.id
                             WHERE rp.repair_id = ?""",
                    (repair_id,),
                )
                parts = c.fetchall()
                parts_str = ", ".join([f"{name}×{qty}" for name, qty in parts])

                row_idx = self.table.rowCount()
                self.table.insertRow(row_idx)
                for col, val in enumerate(row):
                    self.table.setItem(
                        row_idx, col, QtWidgets.QTableWidgetItem(str(val))
                    )
                self.table.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(parts_str))
                self.table.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(row[5]))
        conn.close()

    def generate_invoice(self, row, column):
        repair_id = int(self.table.item(row, 0).text())
        from invoice import InvoiceGenerator

        InvoiceGenerator(repair_id)
        QtWidgets.QMessageBox.information(
            self, "فاکتور", f"فاکتور تعمیر {repair_id} صادر شد."
        )
