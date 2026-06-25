from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

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
        self.lblQuenMatKhau = find_required(self.window, QLabel, "lblQuenMatKhau")
        self.txtUsername = find_required(self.window, QLineEdit, "txtUsername")
        self.txtPassword = find_required(self.window, QLineEdit, "txtPassword")
        self.btnDangNhap = find_required(self.window, QPushButton, "btnDangNhap")

        self.lblTieuDe.setText("ĐĂNG NHẬP HỆ THỐNG")
        self.lblPhuDe.setText("Hệ thống mô phỏng hàng đợi dịch vụ")
        self.lblThongBao.setText("")
        self.lblThongBao.setStyleSheet("""
            QLabel {
                color: #dc2626;
                font-size: 14px;
                font-weight: 600;
                border: none;
                background: transparent;
            }
        """)

        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.lblQuenMatKhau.setText(
            '<a href="forgot-password" style="color:#0d6efd; text-decoration:none;">'
            "Quên mật khẩu?</a>"
        )
        self.lblQuenMatKhau.setTextFormat(Qt.RichText)
        self.lblQuenMatKhau.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.lblQuenMatKhau.setFocusPolicy(Qt.NoFocus)
        self.lblQuenMatKhau.setOpenExternalLinks(False)
        self.lblQuenMatKhau.setCursor(Qt.PointingHandCursor)
        self.lblQuenMatKhau.linkActivated.connect(self.quen_mat_khau)

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

    def quen_mat_khau(self, link=None):
        dialog = QDialog(self.window)
        dialog.setWindowTitle("Quên mật khẩu")
        dialog.setFixedSize(420, 170)

        layout = QVBoxLayout(dialog)

        label = QLabel("Vui lòng liên hệ với Admin để cấp lại mật khẩu.")
        label.setAlignment(Qt.AlignCenter)

        btn_ok = QPushButton("OK")
        btn_ok.setFixedSize(90, 36)
        btn_ok.clicked.connect(dialog.accept)

        layout.addStretch()
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(btn_ok, alignment=Qt.AlignCenter)
        layout.addStretch()

        dialog.exec()
