from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

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
        self._tao_nut_quen_mat_khau()

        self.btnDangNhap.clicked.connect(self.dang_nhap)
        self.txtUsername.returnPressed.connect(self.dang_nhap)
        self.txtPassword.returnPressed.connect(self.dang_nhap)

    def _tao_nut_quen_mat_khau(self):
        self.lblQuenMatKhau.hide()

        self.btnQuenMatKhau = QPushButton("Quên mật khẩu?", self.lblQuenMatKhau.parent())
        self.btnQuenMatKhau.setGeometry(self.lblQuenMatKhau.geometry())
        self.btnQuenMatKhau.setCursor(Qt.PointingHandCursor)
        self.btnQuenMatKhau.setFocusPolicy(Qt.NoFocus)
        self.btnQuenMatKhau.setFlat(True)
        self.btnQuenMatKhau.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #0d6efd;
                font-size: 14px;
                text-align: right;
                padding: 0px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.btnQuenMatKhau.clicked.connect(self.quen_mat_khau)
        self.btnQuenMatKhau.raise_()

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

    def quen_mat_khau(self):
        dialog = QDialog(self.window)
        dialog.setWindowTitle("Quên mật khẩu")
        dialog.setModal(True)
        dialog.setFixedSize(520, 220)
        dialog.setStyleSheet("""
            QDialog {
                background: #f1f7ff;
                font-family: 'Segoe UI';
            }
            QLabel {
                color: #111827;
                font-size: 15px;
                border: none;
                background: transparent;
            }
            QPushButton {
                background: #1769dc;
                color: white;
                border: 1px solid #0f5dc8;
                border-radius: 7px;
                min-width: 112px;
                min-height: 46px;
                font-size: 16px;
                font-weight: 700;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(22)

        message = QLabel("Vui lòng liên hệ với Admin để cấp lại mật khẩu.")
        message.setAlignment(Qt.AlignCenter)

        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(dialog.accept)

        layout.addStretch()
        layout.addWidget(message)
        layout.addWidget(btn_ok, alignment=Qt.AlignCenter)
        layout.addStretch()

        dialog.exec()
