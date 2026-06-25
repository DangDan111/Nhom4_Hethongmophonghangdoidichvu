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
        self.thoi_gian_den = thoi_gian_den or datetime.now()
        self.thoi_gian_bat_dau_phuc_vu = thoi_gian_bat_dau_phuc_vu
        self.thoi_gian_ket_thuc = thoi_gian_ket_thuc
        self.trang_thai = trang_thai
        self.so_tien_giao_dich = so_tien_giao_dich
        self.muc_do_hai_long = muc_do_hai_long

    def tinh_thoi_gian_cho(self):
        if self.thoi_gian_bat_dau_phuc_vu is None:
            moc_tinh = datetime.now()
        else:
            moc_tinh = self.thoi_gian_bat_dau_phuc_vu
        return max(0, (moc_tinh - self.thoi_gian_den).total_seconds() / 60)

    def tinh_thoi_gian_phuc_vu(self):
        if self.thoi_gian_bat_dau_phuc_vu is None or self.thoi_gian_ket_thuc is None:
            return 0
        return max(0, (self.thoi_gian_ket_thuc - self.thoi_gian_bat_dau_phuc_vu).total_seconds() / 60)

    def la_khach_uu_tien(self):
        return self.muc_do_uu_tien < 5

    def ma_khach(self):
        return f"KH{self.id:03d}"
