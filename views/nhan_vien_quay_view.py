from datetime import datetime
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from views.ui_helpers import confirm_logout, fill_table, find_required, load_ui, setup_table


class NhanVienQuayView:
    def __init__(self, ui_path, app_context, on_logout):
        self.app_context = app_context
        self.on_logout = on_logout

        self.user = app_context.get_current_user()
        self.he_thong = app_context.get_he_thong_hang_doi()
        self.quay_id = self.user.quay_id or 1

        self.window = load_ui(ui_path)
        self.window.setFixedSize(1500, 780)

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
        self.lblKhachChoCount = find_required(self.window, QLabel, "lblKhachChoCount")
        self.lblDaPhucVuCount = find_required(self.window, QLabel, "lblDaPhucVuCount")
        self.lblMaQuay = find_required(self.window, QLabel, "lblMaQuay")
        self.lblTrangThaiMo = find_required(self.window, QLabel, "lblTrangThaiMo")
        self.lblTinhTrang = find_required(self.window, QLabel, "lblTinhTrang")
        self.lblTongLuot = find_required(self.window, QLabel, "lblTongLuot")
        self.lblKhachCuoi = find_required(self.window, QLabel, "lblKhachCuoi")
        self.lblTgTb = find_required(self.window, QLabel, "lblTgTb")
        self.lblHieuSuat = find_required(self.window, QLabel, "lblHieuSuat")

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
        self.tblHangDoiUuTien = find_required(
            self.window,
            QTableWidget,
            "tbl_priority_queue"
        )
        self.tblHangDoiThuong = find_required(
            self.window,
            QTableWidget,
            "tbl_normal_queue"
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
        setup_table(
            self.tblHangDoiUuTien,
            ["Mã KH","Tên khách","Ưu tiên","TG chờ"]
        )
        setup_table(
            self.tblHangDoiThuong,
            ["Mã KH","Tên khách","Ưu tiên","TG chờ"]
        )

        self.btnGoiKhach.clicked.connect(
            self.goi_khach
        )

        self.btnHoanThanh.clicked.connect(
            self.hoan_thanh
        )

        self.btnDangXuat.clicked.connect(
            self.xac_nhan_dang_xuat
        )
        self.timer = QTimer(self.window)
        self.timer.timeout.connect(self.lam_moi)
        self.timer.start(1000)   # cập nhật mỗi 1 giây

        self.lam_moi()

    def show(self):
        self.window.show()

    def xac_nhan_dang_xuat(self):
        if confirm_logout(self.window):
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
        tk = self.he_thong.tinh_thong_ke()
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
        self.lblKhachChoCount.setText(str(tk["tong_khach_dang_cho"]))
        self.lblDaPhucVuCount.setText(str(len(quay.lich_su_phuc_vu)))
        self.lblMaQuay.setText(f"Mã quầy: Q{quay.id_quay:02d}")
        self.lblTrangThaiMo.setText(f"Trạng thái mở: {mo_dong}")
        self.lblTinhTrang.setText(f"Tình trạng: {quay.trang_thai}")
        self.lblTongLuot.setText(f"Tổng lượt: {len(quay.lich_su_phuc_vu)}")

        khach = quay.khach_dang_phuc_vu

        if khach is None:
            self.txtKhachDangPhucVu.setPlainText(
                "Hiện chưa có khách hàng nào đang phục vụ."
            )
        else:

            tg_cho = khach.dinh_dang_thoi_gian_cho()
            tg_phuc_vu = khach.dinh_dang_thoi_gian_phuc_vu()

            self.txtKhachDangPhucVu.setPlainText(
                f"Mã khách: {khach.ma_khach()}\n"
                f"Tên khách: {khach.ten}\n"
                f"Loại dịch vụ: {khach.loai_dich_vu}\n"
                f"Mức ưu tiên: {khach.muc_do_uu_tien}\n\n"

                f"Thời gian đến:\n"
                f"{khach.thoi_gian_den.strftime('%H:%M:%S')}\n\n"

                f"Bắt đầu phục vụ:\n"
                f"{khach.thoi_gian_bat_dau_phuc_vu.strftime('%H:%M:%S')}\n\n"

                f"Thời gian chờ:\n"
                f"{tg_cho}\n\n"

                f"Thời gian phục vụ:\n"
                f"{tg_phuc_vu}"
            )

        if len(quay.lich_su_phuc_vu) == 0:
            self.lblKhachCuoi.setText("Khách cuối: -")
            self.lblTgTb.setText("TG TB: 0.0 phút")
        else:
            khach_cuoi = quay.lich_su_phuc_vu[-1]
            tg_tb = sum(
                k.tinh_thoi_gian_phuc_vu()
                for k in quay.lich_su_phuc_vu
            ) / 60 / len(quay.lich_su_phuc_vu)
            self.lblKhachCuoi.setText(f"Khách cuối: {khach_cuoi.ma_khach()}")
            self.lblTgTb.setText(f"TG TB: {tg_tb:.1f} phút")

        if not quay.dang_mo:
            self.lblHieuSuat.setText("● Đang đóng")
            self.lblHieuSuat.setStyleSheet("""
                QLabel{
    background:#FEE2E2;
    color:#DC2626;
    border:1px solid #FCA5A5;
    border-radius:12px;
    padding:4px 10px;
    font-size:12pt;
    font-weight:700;
}
             """)
        elif khach is not None:
            self.lblHieuSuat.setText("● Đang phục vụ")
            self.lblHieuSuat.setStyleSheet("""
        QLabel{
            background-color:#DCFCE7;
            color:#16A34A;
            border:1px solid #86EFAC;
            border-radius:14px;
            padding:6px 14px;
            font-size:13pt;
            font-weight:bold;
        }
    """)
        else:
            self.lblHieuSuat.setText("● Sẵn sàng")
            self.lblHieuSuat.setStyleSheet("""
        QLabel{
            background-color:#FFF7ED;
            color:#EA580C;
            border:1px solid #FDBA74;
            border-radius:14px;
            padding:6px 14px;
            font-size:13pt;
            font-weight:bold;
        }
    """)
        fill_table(
            self.tblHangDoiUuTien,
            self._rows_khach_cho(self.he_thong.lay_danh_sach_hang_doi_uu_tien())
        )
        fill_table(
            self.tblHangDoiThuong,
            self._rows_khach_cho(self.he_thong.lay_danh_sach_hang_doi_thuong())
        )

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
                    k.dinh_dang_thoi_gian_cho()
                )
            )

            self.tblLichSuPhucVu.setItem(
                row,
                4,
                QTableWidgetItem(
                    k.dinh_dang_thoi_gian_phuc_vu()
                )
            )

            self.tblLichSuPhucVu.setItem(
                row,
                5,
                QTableWidgetItem(
                    "Hoàn thành"
                )
            )

    def _rows_khach_cho(self, ds):
        rows = []

        for k in ds:
            rows.append([
                k.ma_khach(),
                k.ten,
                k.muc_do_uu_tien,
                k.dinh_dang_thoi_gian_cho()
            ])

        return rows

    