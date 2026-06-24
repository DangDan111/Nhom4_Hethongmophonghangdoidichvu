from PySide6.QtWidgets import QLabel, QPushButton, QComboBox, QTableWidget, QMessageBox

from views.ui_helpers import fill_table, find_required, load_ui, setup_table


class QuanLyView:
    def __init__(self, ui_path, app_context, on_logout):
        self.app_context = app_context
        self.on_logout = on_logout
        self.user = app_context.get_current_user()
        self.he_thong = app_context.get_he_thong_hang_doi()
        self.window = load_ui(ui_path)
        self.window.setFixedSize(1500, 780)
        self.bao_cao_da_sap_xep = False

        self.lblTaiKhoan = find_required(self.window, QLabel, "lblTaiKhoan")
        self.lblTongDaPhucVu = find_required(self.window, QLabel, "lblTongDaPhucVu")
        self.lblKhachDangCho = find_required(self.window, QLabel, "lblKhachDangCho")
        self.lblQuayDangMo = find_required(self.window, QLabel, "lblQuayDangMo")
        self.lblQuayDangBan = find_required(self.window, QLabel, "lblQuayDangBan")
        self.lblThoiGianChoTB = find_required(self.window, QLabel, "lblThoiGianChoTB")
        self.lblCanhBao = find_required(self.window, QLabel, "lblCanhBao")

        self.tblHangDoiUuTien = find_required(self.window, QTableWidget, "tblHangDoiUuTien")
        self.tblHangDoiThuong = find_required(self.window, QTableWidget, "tblHangDoiThuong")
        self.tblQuay = find_required(self.window, QTableWidget, "tblQuay")
        self.tblBaoCao = find_required(self.window, QTableWidget, "tblBaoCao")

        self.cboQuay = find_required(self.window, QComboBox, "cboQuay")
        self.btnMoQuay = find_required(self.window, QPushButton, "btnMoQuay")
        self.btnDongQuay = find_required(self.window, QPushButton, "btnDongQuay")
        self.btnLamMoi = find_required(self.window, QPushButton, "btnLamMoi")
        self.btnSapXepBaoCao = find_required(self.window, QPushButton, "btnSapXepBaoCao")
        self.btnDangXuat = find_required(self.window, QPushButton, "btnDangXuat")

        self.lblTaiKhoan.setText(f"Tài khoản: {self.user.username}")

        self.cboQuay.clear()
        self.cboQuay.addItems(["Quầy 1", "Quầy 2", "Quầy 3"])

        setup_table(
            self.tblHangDoiUuTien,
            ["Mã KH", "Tên khách", "Dịch vụ", "Ưu tiên", "Thời gian đến"]
        )

        setup_table(
            self.tblHangDoiThuong,
            ["Mã KH", "Tên khách", "Dịch vụ", "Ưu tiên", "Thời gian đến"]
        )

        setup_table(
            self.tblQuay,
            ["Quầy", "Mở/Đóng", "Trạng thái", "Khách đang phục vụ"]
        )

        setup_table(
            self.tblBaoCao,
            ["Mã KH", "Tên khách", "Loại dịch vụ", "Thời gian chờ", "Thời gian phục vụ", "Trạng thái"]
        )

        self.btnMoQuay.clicked.connect(self.mo_quay)
        self.btnDongQuay.clicked.connect(self.dong_quay)
        self.btnLamMoi.clicked.connect(self.lam_moi)
        self.btnSapXepBaoCao.clicked.connect(self.sap_xep_bao_cao)
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

    def lam_moi(self):
        tk = self.he_thong.tinh_thong_ke()

        self.lblTongDaPhucVu.setText(str(tk["tong_khach_da_phuc_vu"]))
        self.lblKhachDangCho.setText(str(tk["tong_khach_dang_cho"]))
        self.lblQuayDangMo.setText(str(tk["so_quay_dang_mo"]))
        self.lblQuayDangBan.setText(str(tk["so_quay_dang_ban"]))
        self.lblThoiGianChoTB.setText(f"{tk['thoi_gian_cho_trung_binh']:.1f} phút")

        self.lblCanhBao.setText("Quá tải" if tk["canh_bao"] else "Ổn định")
        self.lblCanhBao.setStyleSheet(
            "color: #dc2626;" if tk["canh_bao"] else "color: #16a34a;"
        )

        fill_table(
            self.tblHangDoiUuTien,
            self._rows_khach(self.he_thong.lay_danh_sach_hang_doi_uu_tien())
        )

        fill_table(
            self.tblHangDoiThuong,
            self._rows_khach(self.he_thong.lay_danh_sach_hang_doi_thuong())
        )

        fill_table(
            self.tblQuay,
            self._rows_quay()
        )

        if self.bao_cao_da_sap_xep:
            ds = self.he_thong.sap_xep_bao_cao_theo_thoi_gian_cho()
        else:
            ds = self.he_thong.lay_danh_sach_da_phuc_vu()

        fill_table(
            self.tblBaoCao,
            self._rows_bao_cao(ds)
        )

    def sap_xep_bao_cao(self):
        self.bao_cao_da_sap_xep = True
        self.lam_moi()

    def mo_quay(self):
        ok, msg = self.he_thong.mo_quay(self._selected_quay())

        if ok:
            QMessageBox.information(self.window, "Thông báo", msg)
        else:
            QMessageBox.warning(self.window, "Thông báo", msg)

        self.lam_moi()

    def dong_quay(self):
        ok, msg = self.he_thong.dong_quay(self._selected_quay())

        if ok:
            QMessageBox.information(self.window, "Thông báo", msg)
        else:
            QMessageBox.warning(self.window, "Thông báo", msg)

        self.lam_moi()

    def _selected_quay(self):
        return int(self.cboQuay.currentText().replace("Quầy ", ""))

    def _rows_khach(self, ds):
        rows = []

        for k in ds:
            rows.append([
                k.ma_khach(),
                k.ten,
                k.loai_dich_vu,
                k.muc_do_uu_tien,
                k.thoi_gian_den.strftime("%H:%M:%S")
            ])

        return rows

    def _rows_quay(self):
        rows = []

        for q in self.he_thong.lay_danh_sach_quay():
            if q.khach_dang_phuc_vu is None:
                khach = "-"
            else:
                khach = q.khach_dang_phuc_vu.ma_khach()

            rows.append([
                f"Quầy {q.id_quay}",
                "Mở" if q.dang_mo else "Đóng",
                q.trang_thai,
                khach
            ])

        return rows

    def _rows_bao_cao(self, ds):
        rows = []

        for k in ds:
            rows.append([
                k.ma_khach(),
                k.ten,
                k.loai_dich_vu,
                f"{k.tinh_thoi_gian_cho():.1f} phút",
                f"{k.tinh_thoi_gian_phuc_vu():.1f} phút",
                k.trang_thai
            ])

        return rows