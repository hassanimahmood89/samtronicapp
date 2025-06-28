from PyQt5 import QtWidgets, QtGui, QtCore
from database import init_db
from customers import CustomerManager
from repairs import RepairManager
from inventory import InventoryManager
from report import ReportGenerator
from login import LoginWindow
import sys
import os


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مدیریت تعمیرگاه Samtronic")
        self.setGeometry(200, 200, 900, 600)
        self.setWindowIcon(QtGui.QIcon("static/samtronic_logo.png"))

        font_path = os.path.join("fonts", "IRANSans.ttf")
        if os.path.exists(font_path):
            font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
            family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QtGui.QFont(family, 10)
            self.setFont(font)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel("سامانه مدیریت تعمیرگاه Samtronic")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        customer_btn = QtWidgets.QPushButton("مدیریت مشتری‌ها")
        customer_btn.clicked.connect(self.open_customer_window)
        layout.addWidget(customer_btn)

        repair_btn = QtWidgets.QPushButton("ثبت تعمیرات")
        repair_btn.clicked.connect(self.open_repair_window)
        layout.addWidget(repair_btn)

        inventory_btn = QtWidgets.QPushButton("مدیریت انبار")
        inventory_btn.clicked.connect(self.open_inventory_window)
        layout.addWidget(inventory_btn)

        report_btn = QtWidgets.QPushButton("📊 گزارش‌گیری")
        report_btn.clicked.connect(self.generate_report)
        layout.addWidget(report_btn)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_customer_window(self):
        self.customer_window = CustomerManager()
        self.customer_window.show()

    def open_repair_window(self):
        self.repair_window = RepairManager()
        self.repair_window.show()

    def open_inventory_window(self):
        self.inventory_window = InventoryManager()
        self.inventory_window.show()

    def generate_report(self):
        ReportGenerator().generate()


iif __name__ == "__main__":
    init_db()
    app = QtWidgets.QApplication(sys.argv)

    def launch_main():
        window = MainWindow()
        window.show()

    login = LoginWindow(launch_main)
    login.show()

    sys.exit(app.exec_())
