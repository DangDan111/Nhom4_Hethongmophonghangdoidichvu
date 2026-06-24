from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton

from services.auth_service import AuthService
from views.ui_helpers import find_required, load_ui


class LoginView:
    def __init__(self, ui_path, app_context, on_login_success):
        self.app_context = app_context
        self.on_login_success = on_login_success
        self.auth_service = AuthService()
        self.window = load_ui(ui_path)
        self.window.setFixedSize(1280, 720)

        self.lblTieuDe = find_required(self.window, QLabel, "lblTieuDe")
        self.lblPhuDe = find_required(self.window, QLabel, "lblPhuDe")
        self.lblThongBao = find_required(self.window, QLabel, "lblThongBao")
        self.txtUsername = find_required(self.window, QLineEdit, "txtUsername")
        self.txtPassword = find_required(self.window, QLineEdit, "txtPassword")
        self.btnDangNhap = find_required(self.window, QPushButton, "btnDangNhap")

        self.lblTieuDe.setText("ĐĂNG NHẬP HỆ THỐNG")
        self.lblPhuDe.setText("Hệ thống mô phỏng hàng đợi dịch vụ")
        self.lblThongBao.setText("")
        self.lblThongBao.setStyleSheet("color: #dc2626; font-weight: 600;")
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.btnDangNhap.clicked.connect(self.dang_nhap)
        self.txtUsername.returnPressed.connect(self.dang_nhap)
        self.txtPassword.returnPressed.connect(self.dang_nhap)

    def show(self):
        self.window.show()
        self.txtUsername.setFocus(Qt.OtherFocusReason)

    def dang_nhap(self):
        username = self.txtUsername.text().strip()
        password = self.txtPassword.text().strip()
        user, message = self.auth_service.dang_nhap(username, password)
        if user is None:
            self.lblThongBao.setText(message)
            return
        self.app_context.set_current_user(user)
        self.on_login_success()
