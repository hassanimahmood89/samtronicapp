from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

class LoginWindow(QtWidgets.QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle("ورود به سیستم")
        self.setGeometry(400, 250, 300, 150)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()

        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("نام کاربری")
        layout.addWidget(self.username_input)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("رمز عبور")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_btn = QtWidgets.QPushButton("ورود")
        login_btn.clicked.connect(self.check_login)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # 🔐 اینجا می‌تونی چک واقعی با دیتابیس بذاری
        if username == "admin" and password == "1234":
            self.on_login_success()
            self.close()
        else:
            QMessageBox.warning(self, "خطا", "نام کاربری یا رمز اشتباه است")