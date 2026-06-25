from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListView,
    QPushButton,
    QComboBox,
    QTableWidget,
    QHeaderView,
    QTextEdit,
    QVBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import QTimer
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
        self.tblQuay = find_required(self.window, QTableWidget, "tblQuay")
        self.tblBaoCao = find_required(self.window, QTableWidget, "tblBaoCao")

        self.cboQuay = find_required(self.window, QComboBox, "cboQuay")
        self.cboLoaiKhachHang = find_required(self.window, QComboBox, "cboLoaiKhachHang")
        self.cboLocDichVu = find_required(self.window, QComboBox, "cboLocDichVu")
        self.cboThongKeThoiGian = find_required(self.window, QComboBox, "cboThongKeThoiGian")
        self.cboThongKeQuay = find_required(self.window, QComboBox, "cboThongKeQuay")
        self.txtThongKeChiTiet = find_required(self.window, QTextEdit, "txtThongKeChiTiet")
        self.frameBoLocHangDoi = find_required(self.window, QFrame, "frameBoLocHangDoi")
        self.lblLoaiKhachHang = find_required(self.window, QLabel, "lblLoaiKhachHang")
        self.lblDichVuLoc = find_required(self.window, QLabel, "lblDichVuLoc")
        self.btnMoQuay = find_required(self.window, QPushButton, "btnMoQuay")
        self.btnDongQuay = find_required(self.window, QPushButton, "btnDongQuay")
        self.btnLamMoi = find_required(self.window, QPushButton, "btnLamMoi")
        self.btnSapXepBaoCao = find_required(self.window, QPushButton, "btnSapXepBaoCao")
        self.btnDangXuat = find_required(self.window, QPushButton, "btnDangXuat")

        self.lblTaiKhoan.setText(f"Tài khoản: {self.user.username}")

        self.setup_combo_quay()
        self.setup_combo_loc()
        self.setup_combo_thong_ke()
        self.setup_bang()
        self.setup_giao_dien_bo_loc()

        self.btnMoQuay.clicked.connect(self.mo_quay)
        self.btnDongQuay.clicked.connect(self.dong_quay)
        self.btnLamMoi.clicked.connect(self.lam_moi)
        self.btnSapXepBaoCao.clicked.connect(self.sap_xep_bao_cao)
        self.btnDangXuat.clicked.connect(self.xac_nhan_dang_xuat)

        self.cboLoaiKhachHang.currentIndexChanged.connect(self.loc_hang_doi)
        self.cboLocDichVu.currentIndexChanged.connect(self.loc_hang_doi)
        self.cboThongKeThoiGian.currentTextChanged.connect(self.cap_nhat_thong_ke_chi_tiet)
        self.cboThongKeQuay.currentTextChanged.connect(self.cap_nhat_thong_ke_chi_tiet)

        self.tblQuay.cellClicked.connect(self.chon_quay_tu_bang)

        self.lam_moi()

    def setup_combo_quay(self):
        self.cboQuay.clear()

        for q in self.he_thong.lay_danh_sach_quay():
            self.cboQuay.addItem(f"Quầy {q.id_quay}")

    def setup_combo_loc(self):
        self.cboLoaiKhachHang.clear()
        self.cboLoaiKhachHang.addItems([
            "Tất cả",
            "Ưu tiên",
            "Thường",
        ])

        self.cboLocDichVu.clear()
        self.cboLocDichVu.addItems([
            "Tất cả",
            "Giao dịch nhanh",
            "Giao dịch phức tạp",
            "Tư vấn dịch vụ",
            "VIP",
            "Khẩn cấp",
            "Người cao tuổi",
        ])

    def setup_combo_thong_ke(self):
        self.cboThongKeThoiGian.clear()
        self.cboThongKeThoiGian.addItems([
            "Tất cả",
            "Hôm nay",
            "Tuần này",
            "Tháng này",
        ])

        self.cboThongKeQuay.clear()
        self.cboThongKeQuay.addItem("Tất cả")
        for q in self.he_thong.lay_danh_sach_quay():
            self.cboThongKeQuay.addItem(f"Quầy {q.id_quay}")

    def setup_bang(self):
        setup_table(
            self.tblHangDoiUuTien,
            ["Mã KH", "Tên khách", "Dịch vụ", "Loại khách", "Thời gian đến", "Vị trí"]
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
        self._chinh_do_rong_bang_quay()
        self._chinh_do_rong_bang_bao_cao()
    def setup_giao_dien_bo_loc(self):
        self.frameBoLocHangDoi.setFixedHeight(58)

        self.lblLoaiKhachHang.setFixedSize(125, 34)
        self.cboLoaiKhachHang.setFixedSize(110, 34)
        self.lblDichVuLoc.setFixedSize(58, 34)
        self.cboLocDichVu.setFixedSize(185, 34)
        self._setup_combo_dich_vu_style()
        self.txtThongKeChiTiet.setReadOnly(True)
        self.txtThongKeChiTiet.setTextInteractionFlags(
            Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard
        )

        self.lam_moi()
        # Tự động đồng bộ dữ liệu
        self.timer = QTimer(self.window)
        self.timer.timeout.connect(self.lam_moi)
        self.timer.start(1000)

        self.lblLoaiKhachHang.move(12, 12)
        self.cboLoaiKhachHang.move(140, 12)
        self.lblDichVuLoc.move(265, 12)
        self.cboLocDichVu.move(325, 12)

        self.lblLoaiKhachHang.raise_()
        self.cboLoaiKhachHang.raise_()
        self.lblDichVuLoc.raise_()
        self.cboLocDichVu.raise_()

    def _setup_combo_dich_vu_style(self):
        self.cboLocDichVu.setMaxVisibleItems(7)
        self.cboLocDichVu.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.cboLocDichVu.setMinimumContentsLength(12)
        self.cboLocDichVu.setStyleSheet("""
            QComboBox#cboLocDichVu {
                background: #ffffff;
                color: #111827;
                border: 1px solid #c8d6eb;
                border-radius: 7px;
                padding-left: 10px;
                padding-right: 30px;
                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: 600;
                min-height: 32px;
                max-height: 34px;
            }
            QComboBox#cboLocDichVu:hover {
                border: 1px solid #0f73df;
            }
            QComboBox#cboLocDichVu::drop-down {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 28px;
                border-left: 1px solid #d8e3f2;
                border-top-right-radius: 7px;
                border-bottom-right-radius: 7px;
                background: #f6f9ff;
            }
            QComboBox#cboLocDichVu::down-arrow {
                image: none;
                width: 0px;
                height: 0px;
            }
        """)

        view = QListView(self.cboLocDichVu)
        view.setObjectName("lstLocDichVu")
        view.setFocusPolicy(Qt.NoFocus)
        view.setMouseTracking(True)
        view.setUniformItemSizes(True)
        view.setMinimumWidth(self.cboLocDichVu.width())
        view.setTextElideMode(Qt.ElideRight)
        view.setStyleSheet("""
            QListView#lstLocDichVu {
                background: #ffffff;
                color: #111827;
                border: 1px solid #c8d6eb;
                border-radius: 7px;
                padding: 4px;
                outline: 0px;
                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: 600;
                selection-background-color: #eef4ff;
                selection-color: #111827;
            }
            QListView#lstLocDichVu::item {
                min-height: 34px;
                padding-left: 10px;
                padding-right: 8px;
                border: 0px;
                color: #111827;
                background: #ffffff;
            }
            QListView#lstLocDichVu::item:hover {
                background: #f2f6fd;
                color: #111827;
                border: 0px;
            }
            QListView#lstLocDichVu::item:selected,
            QListView#lstLocDichVu::item:selected:active,
            QListView#lstLocDichVu::item:selected:!active {
                background: #eef4ff;
                color: #111827;
                border: 0px;
            }
        """)
        self.cboLocDichVu.setView(view)

        self.lblMuiTenDichVu = QLabel("▾", self.cboLocDichVu)
        self.lblMuiTenDichVu.setAlignment(Qt.AlignCenter)
        self.lblMuiTenDichVu.setFixedSize(28, 32)
        self.lblMuiTenDichVu.move(self.cboLocDichVu.width() - 29, 1)
        self.lblMuiTenDichVu.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.lblMuiTenDichVu.setStyleSheet(
            "color: #475569; background: transparent; border: none; font-size: 14px; font-weight: 800;"
        )
        self.lblMuiTenDichVu.raise_()

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
            self._rows_khach_hien_tai()
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
        self._chinh_do_rong_bang_quay()
        self._chinh_do_rong_bang_bao_cao()
        self.cap_nhat_thong_ke_chi_tiet()

    def loc_hang_doi(self):
        fill_table(
            self.tblHangDoiUuTien,
            self._rows_khach_hien_tai()
        )

        self._chinh_do_rong_bang_hang_doi(self.tblHangDoiUuTien)

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
        dialog.setWindowTitle("Thông báo")
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

    def _loai_khach_text(self, k):
        if k.muc_do_uu_tien < 5:
            return "Ưu tiên"
        return "Thường"

    def _dinh_dang_thoi_gian_den(self, k):
        if hasattr(k.thoi_gian_den, "strftime"):
            return k.thoi_gian_den.strftime("%H:%M:%S")

        return str(k.thoi_gian_den)

    def _khop_bo_loc_khach_hien_tai(self, khach):
        loai_chon = self.cboLoaiKhachHang.currentText().strip()
        dich_vu_chon = self.cboLocDichVu.currentText().strip()

        if loai_chon == "Ưu tiên" and not khach.la_khach_uu_tien():
            return False

        if loai_chon == "Thường" and khach.la_khach_uu_tien():
            return False

        if dich_vu_chon != "Tất cả" and khach.loai_dich_vu != dich_vu_chon:
            return False

        return True

    def _rows_khach_hien_tai(self):
        rows = []

        ds_uu_tien = self.he_thong.lay_danh_sach_hang_doi_uu_tien()
        ds_thuong = self.he_thong.lay_danh_sach_hang_doi_thuong()

        for k in ds_uu_tien:
            loai_khach = self._loai_khach_text(k)
            vi_tri = "Đang chờ"

            if not self._khop_bo_loc_khach_hien_tai(k):
                continue

            rows.append([
                k.ma_khach(),
                k.ten,
                k.loai_dich_vu,
                loai_khach,
                self._dinh_dang_thoi_gian_den(k),
                vi_tri
            ])

        for k in ds_thuong:
            loai_khach = self._loai_khach_text(k)
            vi_tri = "Đang chờ"

            if not self._khop_bo_loc_khach_hien_tai(k):
                continue

            rows.append([
                k.ma_khach(),
                k.ten,
                k.loai_dich_vu,
                loai_khach,
                self._dinh_dang_thoi_gian_den(k),
                vi_tri
            ])

        for q in self.he_thong.lay_danh_sach_quay():
            if q.khach_dang_phuc_vu is None:
                continue

            k = q.khach_dang_phuc_vu
            loai_khach = self._loai_khach_text(k)
            vi_tri = f"Quầy {q.id_quay}"

            if not self._khop_bo_loc_khach_hien_tai(k):
                continue

            rows.append([
                k.ma_khach(),
                k.ten,
                k.loai_dich_vu,
                loai_khach,
                self._dinh_dang_thoi_gian_den(k),
                vi_tri
            ])

        return rows

    def _lay_du_lieu_thong_ke_da_loc(self):
        thoi_gian_chon = self.cboThongKeThoiGian.currentText().strip()
        quay_chon = self.cboThongKeQuay.currentText().strip()
        hom_nay = datetime.now().date()
        ds = []

        for khach in self.he_thong.lay_danh_sach_da_phuc_vu():
            thoi_gian_ket_thuc = khach.thoi_gian_ket_thuc

            if thoi_gian_ket_thuc is None:
                continue

            ngay_ket_thuc = thoi_gian_ket_thuc.date()

            if thoi_gian_chon == "Hôm nay" and ngay_ket_thuc != hom_nay:
                continue

            if thoi_gian_chon == "Tuần này":
                tuan_ket_thuc = ngay_ket_thuc.isocalendar()
                tuan_hien_tai = hom_nay.isocalendar()
                if tuan_ket_thuc.year != tuan_hien_tai.year or tuan_ket_thuc.week != tuan_hien_tai.week:
                    continue

            if thoi_gian_chon == "Tháng này":
                if ngay_ket_thuc.year != hom_nay.year or ngay_ket_thuc.month != hom_nay.month:
                    continue

            if quay_chon != "Tất cả":
                id_quay = int(quay_chon.replace("Quầy ", ""))
                if khach.id_quay != id_quay:
                    continue

            ds.append(khach)

        return ds

    def cap_nhat_thong_ke_chi_tiet(self):
        ds = self._lay_du_lieu_thong_ke_da_loc()

        if not ds:
            self._dat_noi_dung_thong_ke("Chưa có dữ liệu thống kê theo bộ lọc hiện tại.")
            return

        so_khach = len(ds)
        tong_tien = sum(k.so_tien_giao_dich for k in ds)
        hai_long_tb = sum(k.muc_do_hai_long for k in ds) / so_khach
        thoi_gian_cho_tb = sum(k.tinh_thoi_gian_cho() for k in ds) / so_khach / 60
        thoi_gian_phuc_vu_tb = sum(k.tinh_thoi_gian_phuc_vu() for k in ds) / so_khach / 60
        khach_cho_lau_nhat = max(ds, key=lambda k: k.tinh_thoi_gian_cho())
        thoi_gian_cho_lau_nhat = khach_cho_lau_nhat.tinh_thoi_gian_cho() / 60

        if thoi_gian_cho_tb > 30:
            goi_y = "Gợi ý vận hành: Cần thêm quầy hoặc ưu tiên xử lý nhóm chờ lâu."
        elif hai_long_tb < 7:
            goi_y = "Gợi ý vận hành: Nên rà soát thời gian phục vụ và chất lượng tư vấn."
        else:
            goi_y = "Gợi ý vận hành: Vận hành ổn định."

        noi_dung = (
            f"Số khách đã phục vụ: {so_khach}\n"
            f"Tổng tiền giao dịch: {tong_tien:,.0f} VNĐ\n".replace(",", ".")
            + f"Mức độ hài lòng trung bình: {hai_long_tb:.1f} / 10\n\n"
            f"Thời gian chờ trung bình: {thoi_gian_cho_tb:.1f} phút\n"
            f"Thời gian phục vụ trung bình: {thoi_gian_phuc_vu_tb:.1f} phút\n\n"
            f"Thời gian chờ lâu nhất: {thoi_gian_cho_lau_nhat:.1f} phút\n"
            f"Khách chờ lâu nhất: {khach_cho_lau_nhat.ma_khach()} - {khach_cho_lau_nhat.ten}\n\n"
            f"{goi_y}"
        )

        self._dat_noi_dung_thong_ke(noi_dung)

    def _dat_noi_dung_thong_ke(self, noi_dung):
        if self.txtThongKeChiTiet.toPlainText() == noi_dung:
            return

        thanh_keo = self.txtThongKeChiTiet.verticalScrollBar()
        vi_tri_cu = thanh_keo.value()
        self.txtThongKeChiTiet.setPlainText(noi_dung)
        thanh_keo.setValue(min(vi_tri_cu, thanh_keo.maximum()))

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
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.setSectionResizeMode(5, QHeaderView.Fixed)

        bang.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        bang.setWordWrap(False)
        bang.setTextElideMode(Qt.ElideRight)
        bang.setColumnWidth(0, 80)
        bang.setColumnWidth(1, 180)
        bang.setColumnWidth(2, 170)
        bang.setColumnWidth(3, 110)
        bang.setColumnWidth(4, 120)
        bang.setColumnWidth(5, 120)

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
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        header.setSectionResizeMode(6, QHeaderView.Fixed)

        self.tblBaoCao.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tblBaoCao.setWordWrap(False)
        self.tblBaoCao.setTextElideMode(Qt.ElideRight)
        self.tblBaoCao.setColumnWidth(0, 80)
        self.tblBaoCao.setColumnWidth(1, 230)
        self.tblBaoCao.setColumnWidth(2, 170)
        self.tblBaoCao.setColumnWidth(3, 75)
        self.tblBaoCao.setColumnWidth(4, 85)
        self.tblBaoCao.setColumnWidth(5, 125)
        self.tblBaoCao.setColumnWidth(6, 85)
