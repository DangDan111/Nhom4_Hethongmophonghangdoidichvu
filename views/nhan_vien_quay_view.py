from PySide6.QtWidgets import QLabel, QPushButton, QTextEdit, QMessageBox

from views.ui_helpers import find_required, load_ui


class NhanVienQuayView:
    def __init__(self, ui_path, app_context, on_logout):
        self.app_context = app_context
        self.on_logout = on_logout
        self.user = app_context.get_current_user()
        self.he_thong = app_context.get_he_thong_hang_doi()
        self.quay_id = self.user.quay_id or 1
        self.window = load_ui(ui_path)
        self.window.setFixedSize(1500, 780)

        self.lblTaiKhoan = find_required(self.window, QLabel, "lblTaiKhoan")
        self.lblQuay = find_required(self.window, QLabel, "lblQuay")
        self.lblTrangThai = find_required(self.window, QLabel, "lblTrangThai")
        self.txtKhachDangPhucVu = find_required(self.window, QTextEdit, "txtKhachDangPhucVu")
        self.txtLichSu = find_required(self.window, QTextEdit, "txtLichSu")
        self.btnGoiKhach = find_required(self.window, QPushButton, "btnGoiKhach")
        self.btnHoanThanh = find_required(self.window, QPushButton, "btnHoanThanh")
        self.btnDangXuat = find_required(self.window, QPushButton, "btnDangXuat")

        self.lblTaiKhoan.setText(f"Tài khoản: {self.user.username}")
        self.lblQuay.setText(f"Quầy {self.quay_id}")
        self.txtKhachDangPhucVu.setReadOnly(True)
        self.txtLichSu.setReadOnly(True)
        self.btnGoiKhach.clicked.connect(self.goi_khach)
        self.btnHoanThanh.clicked.connect(self.hoan_thanh)
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

    def goi_khach(self):
        ok, message, khach = self.he_thong.goi_khach_tiep_theo(self.quay_id)
        if ok:
            QMessageBox.information(self.window, "Thành công", message)
        else:
            QMessageBox.warning(self.window, "Thông báo", message)
        self.lam_moi()

    def hoan_thanh(self):
        ok, message, khach = self.he_thong.hoan_thanh_phuc_vu(self.quay_id)
        if ok:
            QMessageBox.information(self.window, "Thành công", message)
        else:
            QMessageBox.warning(self.window, "Thông báo", message)
        self.lam_moi()

    def lam_moi(self):
        quay = None
        for q in self.he_thong.lay_danh_sach_quay():
            if q.id_quay == self.quay_id:
                quay = q
                break
        if quay is None:
            return

        mo_dong = "Đang mở" if quay.dang_mo else "Đang đóng"
        self.lblTrangThai.setText(f"Trạng thái: {mo_dong} - {quay.trang_thai}")

        khach = quay.khach_dang_phuc_vu
        if khach is None:
            self.txtKhachDangPhucVu.setPlainText("Hiện chưa có khách hàng nào đang phục vụ.")
        else:
            self.txtKhachDangPhucVu.setPlainText(
                f"Mã khách: {khach.ma_khach()}\n"
                f"Tên khách: {khach.ten}\n"
                f"Loại dịch vụ: {khach.loai_dich_vu}\n"
                f"Mức ưu tiên: {khach.muc_do_uu_tien}\n"
                f"Thời gian đến: {khach.thoi_gian_den.strftime('%H:%M:%S')}\n"
                f"Bắt đầu phục vụ: {khach.thoi_gian_bat_dau_phuc_vu.strftime('%H:%M:%S')}"
            )

        if len(quay.lich_su_phuc_vu) == 0:
            self.txtLichSu.setPlainText("Chưa có khách nào hoàn thành tại quầy này.")
        else:
            lines = ["Mã KH   Tên khách                 Dịch vụ              Chờ(phút)  Phục vụ(phút)"]
            for k in quay.lich_su_phuc_vu:
                lines.append(f"{k.ma_khach():<7} {k.ten:<24} {k.loai_dich_vu:<20} {k.tinh_thoi_gian_cho():<9.1f} {k.tinh_thoi_gian_phuc_vu():.1f}")
            self.txtLichSu.setPlainText("\n".join(lines))
