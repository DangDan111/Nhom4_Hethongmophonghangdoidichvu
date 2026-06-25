import sys
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
    "nhom4.hethonghangdoi"
)
from datetime import datetime
from PySide6.QtCore import QTimer
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
from app_context import AppContext
from views.login_view import LoginView
from views.quan_ly_view import QuanLyView
from views.tiep_nhan_view import TiepNhanView
from views.nhan_vien_quay_view import NhanVienQuayView


BASE_DIR = Path(__file__).resolve().parent
UI_DIR = BASE_DIR / "ui"

class AppController:
    def __init__(self):
        self.app_context = AppContext()
        self.current_window = None

    def start(self):
        self.show_login()

    def show_login(self):
        self.app_context.set_current_user(None)
        self._show(LoginView(UI_DIR / "login.ui", self.app_context, self.open_by_role))

    def open_by_role(self):
        user = self.app_context.get_current_user()
        if user is None:
            self.show_login()
            return

        if user.role == "quan_ly":
            self._show(QuanLyView(UI_DIR / "quan_ly.ui", self.app_context, self.show_login))
        elif user.role == "tiep_nhan":
            self._show(TiepNhanView(UI_DIR / "tiep_nhan.ui", self.app_context, self.show_login))
        elif user.role == "nhan_vien_quay":
            self._show(NhanVienQuayView(UI_DIR / "nhan_vien_quay.ui", self.app_context, self.show_login))
        else:
            QMessageBox.warning(None, "Lỗi", "Vai trò tài khoản không hợp lệ")
            self.show_login()

    def _show(self, view):
        old_window = self.current_window.window if self.current_window is not None else None
        self.current_window = view

        icon_path = BASE_DIR / "images" / "logobieutuong.ico"
        self.current_window.window.setWindowIcon(QIcon(str(icon_path)))

        self._center_window(self.current_window.window)
        self.current_window.show()

        if old_window is not None:
            old_window.close()

    def _center_window(self, window):
        screen = QApplication.primaryScreen()
        if screen is None:
            return
        available = screen.availableGeometry()
        x = available.x() + (available.width() - window.width()) // 2
        y = available.y() + (available.height() - window.height()) // 2
        window.move(max(available.x(), x), max(available.y(), y))


def main():
    app = QApplication(sys.argv)

    ICON_PATH = BASE_DIR / "images" / "logobieutuong.ico"
    app.setWindowIcon(QIcon(str(ICON_PATH)))

    app.setStyleSheet("""
        QWidget { font-family: 'Segoe UI'; font-size: 13px; color: #111827; }
        QMainWindow, QWidget#centralwidget { background: #f5f8ff; }

        QPushButton {
            min-height: 32px;
            font-weight: 600;
            border-radius: 6px;
            padding: 6px 12px;
        }

        QTableWidget {
            background: white;
            alternate-background-color: #f8fbff;
            gridline-color: #e5e7eb;
        }

        QHeaderView::section {
            background: #f8fafc;
            font-weight: 600;
            padding: 7px;
            border: 1px solid #e5e7eb;
        }

        QLineEdit, QComboBox {
            min-height: 34px;
            padding: 4px 8px;
            background-color: white;
            color: #111827;
        }

        QMessageBox {
            background-color: white;
        }

        QMessageBox QLabel {
            color: #111827;
            background-color: white;
        }

        QMessageBox QPushButton {
            background-color: #2563eb;
            color: white;
            min-width: 80px;
            min-height: 30px;
            border-radius: 6px;
        }

        QMessageBox QPushButton:hover {
            background-color: #1d4ed8;
        }
    """)

    controller = AppController()
    controller.start()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())

