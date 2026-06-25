from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QTableWidget, QMessageBox

from views.ui_helpers import confirm_logout, fill_table, find_required, load_ui, setup_table


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
        self.lblKhachDaTiepNhanHomNay = find_required(self.window, QLabel, "lblKhachDaTiepNhanHomNay")
        self.lblSoKhachDangCho = find_required(self.window, QLabel, "lblSoKhachDangCho")
        self.lblKhachUuTien = find_required(self.window, QLabel, "lblKhachUuTien")
        self.txtTheoDoi = find_required(self.window, QTextEdit, "txtTheoDoi")
        self.tblKhachVuaTiepNhan = find_required(self.window, QTableWidget, "tblKhachVuaTiepNhan")
        self.tblNhatKy = find_required(self.window, QTableWidget, "tblNhatKy")

        self.service_options = {
            "Giao dịch nhanh - Thường": ("Giao dịch nhanh", 5),
            "Giao dịch phức tạp - Thường": ("Giao dịch phức tạp", 5),
            "Tư vấn dịch vụ - Thường": ("Tư vấn dịch vụ", 5),
            "VIP - Ưu tiên": ("VIP", 1),
            "Khẩn cấp - Ưu tiên": ("Khẩn cấp", 2),
            "Người cao tuổi - Ưu tiên": ("Người cao tuổi", 3),
        }

        self.cboLoaiDichVu.clear()
        self.cboLoaiDichVu.addItems(list(self.service_options.keys()))

        self.lblTaiKhoan.setText(f"Tài khoản: {self.user.username}")
        self.txtTheoDoi.setReadOnly(True)

        setup_table(
            self.tblKhachVuaTiepNhan,
            ["Mã KH", "Tên khách", "Dịch vụ", "Ưu tiên", "Trạng thái"]
        )
        setup_table(
            self.tblNhatKy,
            ["Thời gian", "Nội dung", "Trạng thái"]
        )

        self.btnThemKhach.clicked.connect(self.them_khach)
        self.btnLamMoi.clicked.connect(self.lam_moi)
        self.btnDangXuat.clicked.connect(self.xac_nhan_dang_xuat)

        self.lam_moi()

    def show(self):
        self.window.show()

    def xac_nhan_dang_xuat(self):
        if confirm_logout(self.window):
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
        self.lblKhachDaTiepNhanHomNay.setText(str(tk["tong_khach_da_tiep_nhan"]))
        self.lblSoKhachDangCho.setText(str(tk["tong_khach_dang_cho"]))
        self.lblKhachUuTien.setText(str(tk["so_khach_uu_tien_dang_cho"]))

        text = "HÀNG ĐỢI ƯU TIÊN\n"
        text += self._format_khach(self.he_thong.lay_danh_sach_hang_doi_uu_tien())
        text += "\n\nHÀNG ĐỢI THƯỜNG\n"
        text += self._format_khach(self.he_thong.lay_danh_sach_hang_doi_thuong())

        self.txtTheoDoi.setPlainText(text)
        fill_table(self.tblKhachVuaTiepNhan, self._rows_tiep_nhan_gan_day())
        fill_table(self.tblNhatKy, self._rows_nhat_ky(tk))

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

    def _rows_tiep_nhan_gan_day(self):
        khach_dang_phuc_vu = [
            q.khach_dang_phuc_vu
            for q in self.he_thong.lay_danh_sach_quay()
            if q.khach_dang_phuc_vu is not None
        ]
        khach_dang_cho = (
            self.he_thong.lay_danh_sach_hang_doi_uu_tien()
            + self.he_thong.lay_danh_sach_hang_doi_thuong()
        )
        ds = sorted(khach_dang_phuc_vu + khach_dang_cho, key=lambda k: k.id, reverse=True)

        return [
            [
                k.ma_khach(),
                k.ten,
                k.loai_dich_vu,
                k.muc_do_uu_tien,
                k.trang_thai,
            ]
            for k in ds[:8]
        ]

    def _rows_nhat_ky(self, tk):
        return [
            ["Hiện tại", f"Đã tiếp nhận {tk['tong_khach_da_tiep_nhan']} khách", "Cập nhật"],
            ["Hiện tại", f"{tk['so_khach_uu_tien_dang_cho']} khách ưu tiên đang chờ", "Đang chờ"],
            ["Hiện tại", f"{tk['so_khach_thuong_dang_cho']} khách thường đang chờ", "Đang chờ"],
        ]
