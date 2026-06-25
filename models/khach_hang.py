from datetime import datetime


class KhachHang:
    def __init__(
        self,
        id,
        ten,
        loai_dich_vu,
        muc_do_uu_tien,
        thoi_gian_den=None,
        thoi_gian_bat_dau_phuc_vu=None,
        thoi_gian_ket_thuc=None,
        trang_thai="Đang chờ",
        so_tien_giao_dich=0,
        muc_do_hai_long=0,
    ):
        self.id = id
        self.ten = ten
        self.loai_dich_vu = loai_dich_vu
        self.muc_do_uu_tien = muc_do_uu_tien

        # Thời điểm khách lấy số
        self.thoi_gian_den = thoi_gian_den or datetime.now()

        # Thời điểm bắt đầu phục vụ
        self.thoi_gian_bat_dau_phuc_vu = thoi_gian_bat_dau_phuc_vu

        # Thời điểm kết thúc
        self.thoi_gian_ket_thuc = thoi_gian_ket_thuc

        self.trang_thai = trang_thai
        self.so_tien_giao_dich = so_tien_giao_dich
        self.muc_do_hai_long = muc_do_hai_long

    def tinh_thoi_gian_cho(self):
        """
        Nếu chưa được gọi:
            thời gian chờ = hiện tại - thời gian đến

        Nếu đã được gọi:
            thời gian chờ = thời gian bắt đầu - thời gian đến
            (giữ nguyên)
        """
        if self.thoi_gian_bat_dau_phuc_vu is None:
            moc = datetime.now()
        else:
            moc = self.thoi_gian_bat_dau_phuc_vu

        return max(
            0,
            (moc - self.thoi_gian_den).total_seconds()
        )

    def tinh_thoi_gian_phuc_vu(self):
        """
        Khi đang phục vụ:
            chạy theo thời gian thực

        Khi hoàn thành:
            giữ nguyên
        """
        if self.thoi_gian_bat_dau_phuc_vu is None:
            return 0

        if self.thoi_gian_ket_thuc is None:
            moc = datetime.now()
        else:
            moc = self.thoi_gian_ket_thuc

        return max(
            0,
            (moc - self.thoi_gian_bat_dau_phuc_vu).total_seconds()
        )

    def dinh_dang_thoi_gian_cho(self):
        tong = int(self.tinh_thoi_gian_cho())
        phut = tong // 60
        giay = tong % 60
        return f"{phut:02d}:{giay:02d}"

    def dinh_dang_thoi_gian_phuc_vu(self):
        tong = int(self.tinh_thoi_gian_phuc_vu())
        phut = tong // 60
        giay = tong % 60
        return f"{phut:02d}:{giay:02d}"

    def la_khach_uu_tien(self):
        return self.muc_do_uu_tien < 5

    def ma_khach(self):
        return f"KH{self.id:03d}"