from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from views.ui_helpers import confirm_logout, find_required, load_ui


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

        self.lblKhachDaTiepNhanHomNay = find_required(
            self.window,
            QLabel,
            "lblKhachDaTiepNhanHomNay"
        )
        self.lblSoKhachDangCho = find_required(
            self.window,
            QLabel,
            "lblSoKhachDangCho"
        )

        self.tblHangDoiUuTien = find_required(
            self.window,
            QTableWidget,
            "tblHangDoiUuTien"
        )
        self.tblHangDoiThuong = find_required(
            self.window,
            QTableWidget,
            "tblHangDoiThuong"
        )

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

        self._setup_bang_hang_doi(self.tblHangDoiUuTien)
        self._setup_bang_hang_doi(self.tblHangDoiThuong)

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
        loai_dich_vu, muc_do_uu_tien = self.service_options[
            self.cboLoaiDichVu.currentText()
        ]

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

        self.lblKhachDaTiepNhanHomNay.setText(
            str(tk["tong_khach_da_tiep_nhan"])
        )
        self.lblSoKhachDangCho.setText(
            str(tk["tong_khach_dang_cho"])
        )

        self._do_du_lieu_bang(
            self.tblHangDoiUuTien,
            self.he_thong.lay_danh_sach_hang_doi_uu_tien()
        )

        self._do_du_lieu_bang(
            self.tblHangDoiThuong,
            self.he_thong.lay_danh_sach_hang_doi_thuong()
        )

    def _setup_bang_hang_doi(self, bang):
        bang.setColumnCount(5)
        bang.setHorizontalHeaderLabels([
            "Mã KH",
            "Tên khách",
            "Dịch vụ",
            "Ưu tiên",
            "Đến lúc"
        ])
        bang.verticalHeader().setVisible(False)
        bang.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        bang.setEditTriggers(QTableWidget.NoEditTriggers)
        bang.setSelectionBehavior(QTableWidget.SelectRows)

    def _do_du_lieu_bang(self, bang, ds):
        bang.setRowCount(len(ds))

        for row, k in enumerate(ds):
            bang.setItem(row, 0, QTableWidgetItem(k.ma_khach()))
            bang.setItem(row, 1, QTableWidgetItem(k.ten))
            bang.setItem(row, 2, QTableWidgetItem(k.loai_dich_vu))
            bang.setItem(row, 3, QTableWidgetItem(str(k.muc_do_uu_tien)))
            bang.setItem(
                row,
                4,
                QTableWidgetItem(k.thoi_gian_den.strftime("%H:%M:%S"))
            )