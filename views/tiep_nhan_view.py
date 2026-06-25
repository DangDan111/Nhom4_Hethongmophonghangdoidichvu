from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from views.ui_helpers import confirm_logout, find_required, load_ui


def find_optional(parent, widget_type, object_name):
    return parent.findChild(widget_type, object_name)


class TiepNhanView:
    def __init__(self, ui_path, app_context, on_logout):
        self.app_context = app_context
        self.on_logout = on_logout
        self.user = app_context.get_current_user()
        self.he_thong = app_context.get_he_thong_hang_doi()
        self.window = load_ui(ui_path)
        self.window.setFixedSize(1500, 780)

        self.lblTaiKhoan = find_required(self.window, QLabel, "lblTaiKhoan")
        self.lblKhachDaTiepNhanHomNay = find_required(self.window, QLabel, "lblKhachDaTiepNhanHomNay")
        self.lblSoKhachDangCho = find_required(self.window, QLabel, "lblSoKhachDangCho")
        self.lblThongBaoThanhCong = find_required(self.window, QLabel, "lblThongBaoThanhCong")

        self.txtTenKhach = find_required(self.window, QLineEdit, "txtTenKhach")
        self.txtSoDienThoai = find_required(self.window, QLineEdit, "txtSoDienThoai")
        self.txtGhiChu = find_required(self.window, QTextEdit, "txtGhiChu")

        self.cboLoaiDichVu = find_required(self.window, QComboBox, "cboLoaiDichVu")
        self.cboNhomKhach = find_required(self.window, QComboBox, "cboNhomKhach")
        self.cboMucUuTien = find_required(self.window, QComboBox, "cboMucUuTien")

        self.btnThemKhach = find_required(self.window, QPushButton, "btnThemKhach")
        self.btnLamMoi = find_required(self.window, QPushButton, "btnLamMoi")
        self.btnTaoSoThuTu = find_optional(self.window, QPushButton, "btnTaoSoThuTu")
        self.btnDangXuat = find_required(self.window, QPushButton, "btnDangXuat")

        self.tblKhachVuaTiepNhan = find_required(self.window, QTableWidget, "tblKhachVuaTiepNhan")
        self.tblNhatKy = find_required(self.window, QTableWidget, "tblNhatKy")

        self.service_options = {
            "Giao dịch nhanh": {"nhom": "Thường", "uu_tien": 5},
            "Giao dịch phức tạp": {"nhom": "Thường", "uu_tien": 5},
            "Tư vấn dịch vụ": {"nhom": "Thường", "uu_tien": 5},
            "VIP": {"nhom": "Ưu tiên", "uu_tien": 1},
            "Khẩn cấp": {"nhom": "Ưu tiên", "uu_tien": 2},
            "Người cao tuổi": {"nhom": "Ưu tiên", "uu_tien": 3},
        }

        self.lblTaiKhoan.setText(f"Tài khoản: {self.user.username}")
        self.lblThongBaoThanhCong.setText("")
        self.txtGhiChu.clear()

        self._setup_comboboxes()
        self._setup_tables()

        self.cboLoaiDichVu.currentTextChanged.connect(self._dong_bo_phan_loai)
        self.btnThemKhach.clicked.connect(self.them_khach)
        self.btnLamMoi.clicked.connect(self.lam_moi)
        if self.btnTaoSoThuTu is not None:
            self.btnTaoSoThuTu.hide()
        self.btnDangXuat.clicked.connect(self.xac_nhan_dang_xuat)

        self.lam_moi()

# Đồng bộ dữ liệu mỗi giây
        self.timer = QTimer(self.window)
        self.timer.timeout.connect(lambda: self.lam_moi(False))
        self.timer.start(1000)

    def show(self):
        self.window.show()

    def xac_nhan_dang_xuat(self):
        if confirm_logout(self.window):
            self.on_logout()

    def them_khach(self):
        ten = self.txtTenKhach.text().strip()
        loai_dich_vu = self.cboLoaiDichVu.currentText()
        muc_do_uu_tien = self.cboMucUuTien.currentData()

        ok, message, khach = self.he_thong.them_khach(ten, loai_dich_vu, muc_do_uu_tien)

        if not ok:
            self._hien_thong_bao(message, thanh_cong=False)
            self.lam_moi(reset_form=False)
            return

        self._hien_thong_bao(message, thanh_cong=True)
        self.lam_moi(reset_form=True)

    def lam_moi(self, reset_form=True):
        if reset_form:
            self.txtTenKhach.clear()
            self.txtSoDienThoai.clear()
            self.txtGhiChu.clear()
            self.cboLoaiDichVu.setCurrentIndex(0)
            self._dong_bo_phan_loai(self.cboLoaiDichVu.currentText())
            self.lblThongBaoThanhCong.setText("")

        tk = self.he_thong.tinh_thong_ke()
        self.lblKhachDaTiepNhanHomNay.setText(str(tk["tong_khach_da_tiep_nhan"]))
        self.lblSoKhachDangCho.setText(str(tk["tong_khach_dang_cho"]))

        self._fill_khach_vua_tiep_nhan()
        self._fill_chi_tiet_quay()

    def _setup_comboboxes(self):
        self.cboLoaiDichVu.clear()
        self.cboLoaiDichVu.addItems(list(self.service_options.keys()))

        self.cboNhomKhach.clear()
        self.cboNhomKhach.addItems(["Thường", "Ưu tiên"])
        self.cboNhomKhach.setEnabled(False)

        self.cboMucUuTien.clear()
        for text, value in [
            ("1 - VIP", 1),
            ("2 - Khẩn cấp", 2),
            ("3 - Người cao tuổi", 3),
            ("5 - Thường", 5),
        ]:
            self.cboMucUuTien.addItem(text, value)
        self.cboMucUuTien.setEnabled(False)
        self._dong_bo_phan_loai(self.cboLoaiDichVu.currentText())

    def _setup_tables(self):
        self._setup_table(
    self.tblKhachVuaTiepNhan,
            [
                "Mã KH",
                "Tên khách",
                "Dịch vụ",
                "Nhóm",
                "Quầy",
                "Thời gian"
            ]
        )
        self._setup_table(
            self.tblNhatKy,
            [
                "Quầy",
                "Mở/Đóng",
                "Trạng thái",
                "Khách đang phục vụ",
                "Khách chờ",
                "Đã phục vụ",
                "Gợi ý",
            ],
        )

        self._ap_dung_lai_do_rong_tat_ca_bang()

    def _setup_table(self, table, headers):
        table.clear()
        table.clearSpans()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(0)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(34)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setAlternatingRowColors(True)

    def _cau_hinh_bang_chung(self, table):
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setWordWrap(False)
        table.setTextElideMode(Qt.ElideRight)

        header = table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setMinimumSectionSize(35)

    def _set_fixed_col(self, table, col, width):
        header = table.horizontalHeader()
        header.setSectionResizeMode(col, QHeaderView.Fixed)
        table.setColumnWidth(col, width)

    def _set_stretch_col(self, table, col):
        table.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)

    def _chinh_bang_khach_vua_tiep_nhan(self):
        table = self.tblKhachVuaTiepNhan
        self._cau_hinh_bang_chung(table)

        self._set_fixed_col(table, 0, 75)
        self._set_stretch_col(table, 1)
        self._set_stretch_col(table, 2)
        self._set_fixed_col(table, 3, 90)
        self._set_fixed_col(table, 4, 80)
        self._set_fixed_col(table, 5, 100)

    def _chinh_bang_chi_tiet_quay(self):
        table = self.tblNhatKy
        self._cau_hinh_bang_chung(table)

        self._set_fixed_col(table, 0, 75)
        self._set_fixed_col(table, 1, 90)
        self._set_fixed_col(table, 2, 120)
        self._set_stretch_col(table, 3)
        self._set_fixed_col(table, 4, 90)
        self._set_fixed_col(table, 5, 80)
        self._set_stretch_col(table, 6)

    def _ap_dung_lai_do_rong_bang(self, table):
        if table is self.tblKhachVuaTiepNhan:
            self._chinh_bang_khach_vua_tiep_nhan()

        elif table is self.tblNhatKy:
            self._chinh_bang_chi_tiet_quay()
        elif table is self.tblKhachVuaTiepNhan:
            self._chinh_bang_khach_vua_tiep_nhan()
        elif table is self.tblNhatKy:
            self._chinh_bang_chi_tiet_quay()

    def _ap_dung_lai_do_rong_tat_ca_bang(self):
        self._chinh_bang_khach_vua_tiep_nhan()
        self._chinh_bang_chi_tiet_quay()

    def _dong_bo_phan_loai(self, loai_dich_vu):
        info = self.service_options.get(loai_dich_vu)
        if info is None:
            return
        self.cboNhomKhach.setCurrentText(info["nhom"])
        index = self.cboMucUuTien.findData(info["uu_tien"])
        if index >= 0:
            self.cboMucUuTien.setCurrentIndex(index)

    def _fill_khach_vua_tiep_nhan(self):
        rows = []

        for khach in self._lay_khach_vua_tiep_nhan():

            if getattr(khach, "id_quay", None):
                quay = f"Quầy {khach.id_quay}"
            else:
                quay = "Đang chờ"

            rows.append([
                khach.ma_khach(),
                khach.ten,
                khach.loai_dich_vu,
                "Ưu tiên" if khach.la_khach_uu_tien() else "Thường",
                quay,
                khach.thoi_gian_den.strftime("%H:%M:%S"),
            ])

        self._fill_rows(
            self.tblKhachVuaTiepNhan,
            rows,
            "Chưa có khách vừa tiếp nhận",
        )
    
    def _fill_chi_tiet_quay(self):
        so_uu_tien_cho = len(self.he_thong.lay_danh_sach_hang_doi_uu_tien())
        so_thuong_cho = len(self.he_thong.lay_danh_sach_hang_doi_thuong())
        tong_khach_cho = so_uu_tien_cho + so_thuong_cho
        rows = []

        for quay in self.he_thong.lay_danh_sach_quay():
            khach = quay.khach_dang_phuc_vu
            if khach is None:
                khach_text = "-"
            else:
                khach_text = f"{khach.ma_khach()} - {khach.ten}"

            if not quay.dang_mo:
                goi_y = "Có thể mở khi đông khách"
            elif khach is None and (so_uu_tien_cho + so_thuong_cho) > 0:
                goi_y = "Sẵn sàng gọi khách"
            elif khach is not None:
                goi_y = "Đang xử lý"
            else:
                goi_y = "Rảnh"

            rows.append([
                f"Quầy {quay.id_quay}",
                "Mở" if quay.dang_mo else "Đóng",
                quay.trang_thai,
                khach_text,
                tong_khach_cho,
                len(quay.lich_su_phuc_vu),
                goi_y
            ])

        self._fill_rows(self.tblNhatKy, rows, "Chưa có dữ liệu quầy")

    def _fill_rows(self, table, rows, empty_text):
        table.clearSpans()

        if not rows:
            table.setRowCount(1)

            item = QTableWidgetItem(empty_text)
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(0, 0, item)

            if table.columnCount() > 1:
                table.setSpan(0, 0, 1, table.columnCount())

            self._ap_dung_lai_do_rong_bang(table)
            return

        table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_index, col_index, item)

        self._ap_dung_lai_do_rong_bang(table)

    def _lay_khach_vua_tiep_nhan(self):

        ds = []

        ds.extend(self.he_thong.lay_danh_sach_hang_doi_uu_tien())

        ds.extend(self.he_thong.lay_danh_sach_hang_doi_thuong())

        for quay in self.he_thong.lay_danh_sach_quay():
            if quay.khach_dang_phuc_vu:
                ds.append(quay.khach_dang_phuc_vu)

        # ===== THÊM =====
        ds.extend(self.he_thong.lay_danh_sach_da_phuc_vu())
        # ================

        ds.sort(key=lambda x: x.id, reverse=True)

        return ds[:20]
    def _hien_thong_bao(self, message, thanh_cong=True):
        prefix = "✓" if thanh_cong else "!"
        self.lblThongBaoThanhCong.setText(f"{prefix}   {message}")
        self.lblThongBaoThanhCong.setProperty("status", "" if thanh_cong else "error")
        self.lblThongBaoThanhCong.style().unpolish(self.lblThongBaoThanhCong)
        self.lblThongBaoThanhCong.style().polish(self.lblThongBaoThanhCong)
