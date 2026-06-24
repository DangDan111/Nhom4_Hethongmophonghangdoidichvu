from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QMessageBox

from views.ui_helpers import find_required, load_ui


class TiepNhanView:
    def __init__(self, ui_path, app_context, on_logout):
        self.app_context = app_context
        self.on_logout = on_logout
        self.user = app_context.get_current_user()
        self.he_thong = app_context.get_he_thong_hang_doi()
        self.window = load_ui(ui_path)
        self.window.setFixedSize(1500, 780)

        self.lblTaiKhoan = find_required(self.window, QLabel, "lblTaiKhoan")
        self.txtTenKhach = find_required(self.window, QLineEdit, "txtTenKhach")
        self.cboLoaiDichVu = find_required(self.window, QComboBox, "cboLoaiDichVu")
        self.btnThemKhach = find_required(self.window, QPushButton, "btnThemKhach")
        self.btnLamMoi = find_required(self.window, QPushButton, "btnLamMoi")
        self.btnDangXuat = find_required(self.window, QPushButton, "btnDangXuat")
        self.lblSoKhachDangCho = find_required(self.window, QLabel, "lblSoKhachDangCho")
        self.txtTheoDoi = find_required(self.window, QTextEdit, "txtTheoDoi")

        self.service_options = {
            "Khám tổng quát - Thường": ("Khám tổng quát", 5),
            "Khám da liễu - Thường": ("Khám da liễu", 5),
            "Khám mắt - Thường": ("Khám mắt", 5),
            "VIP - Ưu tiên": ("VIP", 1),
            "Cấp cứu - Ưu tiên": ("Cấp cứu", 2),
            "Người cao tuổi - Ưu tiên": ("Người cao tuổi", 3),
        }

        self.cboLoaiDichVu.clear()
        self.cboLoaiDichVu.addItems(list(self.service_options.keys()))

        self.lblTaiKhoan.setText(f"Tài khoản: {self.user.username}")
        self.txtTheoDoi.setReadOnly(True)

        self.btnThemKhach.clicked.connect(self.them_khach)
        self.btnLamMoi.clicked.connect(self.lam_moi)
        self.btnDangXuat.clicked.connect(self.xac_nhan_dang_xuat)

        self.lam_moi()

    def show(self):
        self.window.show()

    def xac_nhan_dang_xuat(self):
        tra_loi = QMessageBox.question(
            self.window,
            "Xác nhận đăng xuất",
            "Bạn có muốn đăng xuất không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if tra_loi == QMessageBox.StandardButton.Yes:
            self.on_logout()

    def them_khach(self):
        ten = self.txtTenKhach.text().strip()
        loai_dich_vu, muc_do_uu_tien = self.service_options[self.cboLoaiDichVu.currentText()]

        ok, message, khach = self.he_thong.them_khach(
            ten,
            loai_dich_vu,
            muc_do_uu_tien
        )

        if not ok:
            QMessageBox.warning(self.window, "Cảnh báo", message)
            return

        self.txtTenKhach.clear()
        QMessageBox.information(self.window, "Thành công", message)
        self.lam_moi()

    def lam_moi(self):
        tk = self.he_thong.tinh_thong_ke()
        self.lblSoKhachDangCho.setText(str(tk["tong_khach_dang_cho"]))

        text = "HÀNG ĐỢI ƯU TIÊN\n"
        text += self._format_khach(self.he_thong.lay_danh_sach_hang_doi_uu_tien())
        text += "\n\nHÀNG ĐỢI THƯỜNG\n"
        text += self._format_khach(self.he_thong.lay_danh_sach_hang_doi_thuong())

        self.txtTheoDoi.setPlainText(text)

    def _format_khach(self, ds):
        if len(ds) == 0:
            return "Chưa có khách đang chờ."

        lines = [
            "Mã KH   Tên khách                 Dịch vụ              Ưu tiên   Đến lúc"
        ]

        for k in ds:
            lines.append(
                f"{k.ma_khach():<7} "
                f"{k.ten:<24} "
                f"{k.loai_dich_vu:<20} "
                f"{k.muc_do_uu_tien:<8} "
                f"{k.thoi_gian_den.strftime('%H:%M:%S')}"
            )

        return "\n".join(lines)