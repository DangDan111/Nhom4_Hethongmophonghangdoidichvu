from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

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

        # ===== Labels =====
        self.lblTaiKhoan = find_required(
            self.window,
            QLabel,
            "lblTaiKhoan"
        )

        self.lblQuay = find_required(
            self.window,
            QLabel,
            "lblQuay"
        )

        self.lblTrangThai = find_required(
            self.window,
            QLabel,
            "lblTrangThai"
        )

        # ===== Khách đang phục vụ =====
        self.txtKhachDangPhucVu = find_required(
            self.window,
            QTextEdit,
            "txtKhachDangPhucVu"
        )

        # ===== Lịch sử phục vụ =====
        self.tblLichSuPhucVu = find_required(
            self.window,
            QTableWidget,
            "tblLichSuPhucVu"
        )

        # ===== Buttons =====
        self.btnGoiKhach = find_required(
            self.window,
            QPushButton,
            "btn_next_customer"
        )

        self.btnHoanThanh = find_required(
            self.window,
            QPushButton,
            "btn_finish_service"
        )

        self.btnDangXuat = find_required(
            self.window,
            QPushButton,
            "btn_logout"
        )

        # ===== Khởi tạo =====
        self.lblTaiKhoan.setText(
            f"Tài khoản: {self.user.username}"
        )

        self.lblQuay.setText(
            f"Quầy {self.quay_id}"
        )

        self.txtKhachDangPhucVu.setReadOnly(True)

        self.btnGoiKhach.clicked.connect(
            self.goi_khach
        )

        self.btnHoanThanh.clicked.connect(
            self.hoan_thanh
        )

        self.btnDangXuat.clicked.connect(
            self.xac_nhan_dang_xuat
        )

        self.lam_moi()

    def show(self):
        self.window.show()

    def xac_nhan_dang_xuat(self):
        tra_loi = QMessageBox.question(
            self.window,
            "Xác nhận đăng xuất",
            "Bạn có muốn đăng xuất không?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if tra_loi == QMessageBox.StandardButton.Yes:
            self.on_logout()

    def goi_khach(self):
        ok, message, khach = self.he_thong.goi_khach_tiep_theo(
            self.quay_id
        )

        if ok:
            QMessageBox.information(
                self.window,
                "Thành công",
                message
            )
        else:
            QMessageBox.warning(
                self.window,
                "Thông báo",
                message
            )

        self.lam_moi()

    def hoan_thanh(self):
        ok, message, khach = self.he_thong.hoan_thanh_phuc_vu(
            self.quay_id
        )

        if ok:
            QMessageBox.information(
                self.window,
                "Thành công",
                message
            )
        else:
            QMessageBox.warning(
                self.window,
                "Thông báo",
                message
            )

        self.lam_moi()

    def lam_moi(self):
        quay = None

        for q in self.he_thong.lay_danh_sach_quay():
            if q.id_quay == self.quay_id:
                quay = q
                break

        if quay is None:
            return

        mo_dong = (
            "Đang mở"
            if quay.dang_mo
            else "Đang đóng"
        )

        self.lblTrangThai.setText(
            f"{mo_dong}"
        )

        # ==========================
        # Khách đang phục vụ
        # ==========================
        khach = quay.khach_dang_phuc_vu

        if khach is None:
            self.txtKhachDangPhucVu.setPlainText(
                "Hiện chưa có khách hàng nào đang phục vụ."
            )
        else:
            self.txtKhachDangPhucVu.setPlainText(
                f"Mã khách: {khach.ma_khach()}\n"
                f"Tên khách: {khach.ten}\n"
                f"Loại dịch vụ: {khach.loai_dich_vu}\n"
                f"Mức ưu tiên: {khach.muc_do_uu_tien}\n"
                f"Thời gian đến: "
                f"{khach.thoi_gian_den.strftime('%H:%M:%S')}\n"
                f"Bắt đầu phục vụ: "
                f"{khach.thoi_gian_bat_dau_phuc_vu.strftime('%H:%M:%S')}"
            )

        # ==========================
        # Lịch sử phục vụ
        # ==========================
        self.tblLichSuPhucVu.setRowCount(0)

        for row, k in enumerate(
            quay.lich_su_phuc_vu
        ):
            self.tblLichSuPhucVu.insertRow(row)

            self.tblLichSuPhucVu.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(k.ma_khach())
                )
            )

            self.tblLichSuPhucVu.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(k.ten)
                )
            )

            self.tblLichSuPhucVu.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(k.loai_dich_vu)
                )
            )

            self.tblLichSuPhucVu.setItem(
                row,
                3,
                QTableWidgetItem(
                    f"{k.tinh_thoi_gian_cho():.1f}"
                )
            )

            self.tblLichSuPhucVu.setItem(
                row,
                4,
                QTableWidgetItem(
                    f"{k.tinh_thoi_gian_phuc_vu():.1f}"
                )
            )

            self.tblLichSuPhucVu.setItem(
                row,
                5,
                QTableWidgetItem(
                    "Hoàn thành"
                )
            )