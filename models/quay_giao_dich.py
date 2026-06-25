from datetime import datetime


class QuayGiaoDich:
    def __init__(self, id_quay, dang_mo=True):
        self.id_quay = id_quay
        self.dang_mo = dang_mo
        self.trang_thai = "Rảnh" if dang_mo else "Đóng"

        self.khach_dang_phuc_vu = None
        self.lich_su_phuc_vu = []

    def mo_quay(self):
        self.dang_mo = True

        if self.khach_dang_phuc_vu is None:
            self.trang_thai = "Rảnh"

    def dong_quay(self):
        if self.khach_dang_phuc_vu is not None:
            return False

        self.dang_mo = False
        self.trang_thai = "Đóng"
        return True

    def co_the_nhan_khach(self):
        return (
            self.dang_mo
            and self.khach_dang_phuc_vu is None
        )

    def tiep_nhan_khach(self, khach_hang):
        """
        Khi gọi khách tiếp theo.
        Thời gian bắt đầu phục vụ luôn lấy theo thời gian thực.
        """

        if not self.co_the_nhan_khach():
            return False

        khach_hang.thoi_gian_bat_dau_phuc_vu = datetime.now()
        khach_hang.thoi_gian_ket_thuc = None
        khach_hang.trang_thai = "Đang phục vụ"

        self.khach_dang_phuc_vu = khach_hang
        self.trang_thai = "Đang phục vụ"

        return True

    def hoan_thanh_phuc_vu(self):
        """
        Khi nhấn nút Hoàn thành.
        Lưu thời điểm kết thúc để thời gian phục vụ dừng lại.
        """

        if self.khach_dang_phuc_vu is None:
            return None

        khach = self.khach_dang_phuc_vu

        khach.thoi_gian_ket_thuc = datetime.now()
        khach.trang_thai = "Đã phục vụ"

        self.lich_su_phuc_vu.append(khach)

        self.khach_dang_phuc_vu = None

        if self.dang_mo:
            self.trang_thai = "Rảnh"
        else:
            self.trang_thai = "Đóng"

        return khach