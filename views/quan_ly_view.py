from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QTableWidget,
    QHeaderView,
    QVBoxLayout,
)

from views.ui_helpers import confirm_logout, fill_table, find_required, load_ui, setup_table


class QuanLyView:
    def __init__(self, ui_path, app_context, on_logout):
        self.app_context = app_context
        self.on_logout = on_logout
        self.user = app_context.get_current_user()
        self.he_thong = app_context.get_he_thong_hang_doi()
        self.window = load_ui(ui_path)
        self.window.setFixedSize(1500, 780)
        self.che_do_bao_cao = "mac_dinh"

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
            ["Mã KH", "Tên khách", "Loại dịch vụ", "Chờ", "Phục vụ", "Tiền", "Hài lòng"]
        )

        self._chinh_do_rong_bang_hang_doi(self.tblHangDoiUuTien)
        self._chinh_do_rong_bang_hang_doi(self.tblHangDoiThuong)
        self._chinh_do_rong_bang_quay()
        self._chinh_do_rong_bang_bao_cao()

        self.btnMoQuay.clicked.connect(self.mo_quay)
        self.btnDongQuay.clicked.connect(self.dong_quay)
        self.btnLamMoi.clicked.connect(self.lam_moi)
        self.btnSapXepBaoCao.clicked.connect(self.sap_xep_bao_cao)
        self.btnDangXuat.clicked.connect(self.xac_nhan_dang_xuat)
        self.tblQuay.cellClicked.connect(self.chon_quay_tu_bang)

        self.lam_moi()

    def show(self):
        self.window.show()

    def xac_nhan_dang_xuat(self):
        if confirm_logout(self.window):
            self.on_logout()

    def lam_moi(self):
        tk = self.he_thong.tinh_thong_ke()

        self.lblTongDaPhucVu.setText(str(tk["tong_khach_da_phuc_vu"]))
        self.lblKhachDangCho.setText(str(tk["tong_khach_dang_cho"]))
        self.lblQuayDangMo.setText(str(tk["so_quay_dang_mo"]))
        self.lblQuayDangBan.setText(str(tk["so_quay_dang_ban"]))
        self.lblThoiGianChoTB.setText(f"{tk['thoi_gian_cho_trung_binh']:.1f} phút")

        self.lblCanhBao.setText("Cần thêm quầy" if tk["canh_bao"] else "Ổn định")
        self.lblCanhBao.setStyleSheet(
            "color: #dc2626; font-weight: 900; background: transparent; border: none;"
            if tk["canh_bao"]
            else
            "color: #16a34a; font-weight: 900; background: transparent; border: none;"
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

        fill_table(
            self.tblBaoCao,
            self._rows_bao_cao(self._lay_bao_cao())
        )

        self._chinh_do_rong_bang_hang_doi(self.tblHangDoiUuTien)
        self._chinh_do_rong_bang_hang_doi(self.tblHangDoiThuong)
        self._chinh_do_rong_bang_quay()
        self._chinh_do_rong_bang_bao_cao()

    def sap_xep_bao_cao(self):
        if self.che_do_bao_cao == "mac_dinh":
            self.che_do_bao_cao = "thoi_gian_cho"
            self.btnSapXepBaoCao.setText("Sắp xếp theo tiền")
        elif self.che_do_bao_cao == "thoi_gian_cho":
            self.che_do_bao_cao = "so_tien"
            self.btnSapXepBaoCao.setText("Sắp xếp theo hài lòng")
        elif self.che_do_bao_cao == "so_tien":
            self.che_do_bao_cao = "hai_long"
            self.btnSapXepBaoCao.setText("Báo cáo mặc định")
        else:
            self.che_do_bao_cao = "mac_dinh"
            self.btnSapXepBaoCao.setText("Sắp xếp báo cáo")

        self.lam_moi()

    def mo_quay(self):
        ok, msg = self.he_thong.mo_quay(self._selected_quay())
        self._hien_thong_bao(msg, thanh_cong=ok)
        self.lam_moi()

    def dong_quay(self):
        ok, msg = self.he_thong.dong_quay(self._selected_quay())
        self._hien_thong_bao(msg, thanh_cong=ok)
        self.lam_moi()

    def _hien_thong_bao(self, message, thanh_cong=True):
        dialog = QDialog(self.window)
        dialog.setWindowTitle("Th?ng b?o")
        dialog.setModal(True)
        dialog.setFixedSize(440, 220)
        dialog.setStyleSheet("""
            QDialog {
                background: #f8fbff;
                font-family: 'Segoe UI';
            }
            QLabel {
                color: #111827;
                border: none;
                background: transparent;
            }
            QLabel#iconLabel {
                color: white;
                border-radius: 24px;
                font-size: 26px;
                font-weight: 800;
                min-width: 48px;
                min-height: 48px;
                max-width: 48px;
                max-height: 48px;
            }
            QLabel#messageLabel {
                font-size: 16px;
                font-weight: 500;
            }
            QPushButton {
                background: #1769dc;
                color: white;
                border: 1px solid #0f5dc8;
                border-radius: 7px;
                min-width: 138px;
                min-height: 46px;
                font-size: 16px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: #0f5dc8;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(34, 26, 34, 26)
        layout.setSpacing(22)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(18)
        content_layout.addStretch()

        icon = QLabel("i" if thanh_cong else "!")
        icon.setObjectName("iconLabel")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet(
            "background: #1d8fe8;" if thanh_cong else "background: #ef4444;"
        )

        label = QLabel(message)
        label.setObjectName("messageLabel")
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        label.setMinimumWidth(230)

        content_layout.addWidget(icon)
        content_layout.addWidget(label)
        content_layout.addStretch()

        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(dialog.accept)

        layout.addStretch()
        layout.addLayout(content_layout)
        layout.addWidget(btn_ok, alignment=Qt.AlignCenter)
        layout.addStretch()

        dialog.exec()

    def chon_quay_tu_bang(self, row, column):
        item = self.tblQuay.item(row, 0)

        if item is None:
            return

        ten_quay = item.text().strip()
        index = self.cboQuay.findText(ten_quay)

        if index >= 0:
            self.cboQuay.setCurrentIndex(index)

    def _selected_quay(self):
        text = self.cboQuay.currentText().strip()
        return int(text.replace("Quầy ", ""))

    def _lay_bao_cao(self):
        if self.che_do_bao_cao == "thoi_gian_cho":
            return self.he_thong.sap_xep_bao_cao_theo_thoi_gian_cho()

        if self.che_do_bao_cao == "so_tien":
            return self.he_thong.sap_xep_bao_cao_theo_so_tien()

        if self.che_do_bao_cao == "hai_long":
            return self.he_thong.sap_xep_bao_cao_theo_hai_long()

        return self.he_thong.lay_danh_sach_da_phuc_vu()

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
                k.dinh_dang_thoi_gian_cho(),
                k.dinh_dang_thoi_gian_phuc_vu(),
                f"{k.so_tien_giao_dich:,}đ".replace(",", "."),
                f"{k.muc_do_hai_long}/10"
            ])

        return rows

    def _chinh_do_rong_bang_hang_doi(self, bang):
        header = bang.horizontalHeader()
        header.setStretchLastSection(False)

        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Fixed)

        bang.setColumnWidth(0, 85)
        bang.setColumnWidth(3, 60)
        bang.setColumnWidth(4, 115)

    def _chinh_do_rong_bang_quay(self):
        header = self.tblQuay.horizontalHeader()
        header.setStretchLastSection(False)

        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)

        self.tblQuay.setColumnWidth(0, 90)
        self.tblQuay.setColumnWidth(1, 105)
        self.tblQuay.setColumnWidth(3, 135)

    def _chinh_do_rong_bang_bao_cao(self):
        header = self.tblBaoCao.horizontalHeader()
        header.setStretchLastSection(False)

        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        header.setSectionResizeMode(6, QHeaderView.Fixed)

        self.tblBaoCao.setColumnWidth(0, 85)
        self.tblBaoCao.setColumnWidth(3, 95)
        self.tblBaoCao.setColumnWidth(4, 95)
        self.tblBaoCao.setColumnWidth(5, 100)
        self.tblBaoCao.setColumnWidth(6, 90)
