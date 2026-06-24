from models.khach_hang import KhachHang
from models.quay_giao_dich import QuayGiaoDich
from data_structures.linear_queue import LinearQueue
from data_structures.priority_queue_heap import PriorityQueueHeap
from utils.statistics import merge_sort_theo_thoi_gian_cho_giam_dan, tinh_thoi_gian_cho_trung_binh


class HeThongHangDoi:
    def __init__(self):
        self.hang_doi_thuong = LinearQueue(max_size=50)
        self.hang_doi_uu_tien = PriorityQueueHeap()
        self.danh_sach_quay = []
        self.danh_sach_da_phuc_vu = []
        self.next_customer_id = 1

        for id_quay in range(1, 4):
            self.danh_sach_quay.append(QuayGiaoDich(id_quay, dang_mo=True))

    def them_khach(self, ten, loai_dich_vu, muc_do_uu_tien):
        ten = ten.strip()
        loai_dich_vu = loai_dich_vu.strip()

        if ten == "":
            return False, "Vui lòng nhập tên khách hàng", None
        if loai_dich_vu == "":
            return False, "Vui lòng chọn loại dịch vụ", None

        khach = KhachHang(
            id=self.next_customer_id,
            ten=ten,
            loai_dich_vu=loai_dich_vu,
            muc_do_uu_tien=muc_do_uu_tien,
        )
        self.next_customer_id += 1

        if muc_do_uu_tien < 5:
            self.hang_doi_uu_tien.push(khach)
            return True, f"Đã thêm {khach.ma_khach()} vào hàng đợi ưu tiên", khach

        if not self.hang_doi_thuong.enqueue(khach):
            return False, "Hàng đợi thường đã đầy", None
        return True, f"Đã thêm {khach.ma_khach()} vào hàng đợi thường", khach

    def goi_khach_tiep_theo(self, id_quay):
        quay = self._tim_quay(id_quay)
        if quay is None:
            return False, "Không tìm thấy quầy", None
        if not quay.dang_mo:
            return False, "Quầy đang đóng", None
        if not quay.co_the_nhan_khach():
            return False, "Quầy đang phục vụ khách khác", quay.khach_dang_phuc_vu

        khach = self.hang_doi_uu_tien.pop()
        if khach is None:
            khach = self.hang_doi_thuong.dequeue()
        if khach is None:
            return False, "Không còn khách đang chờ", None

        quay.tiep_nhan_khach(khach)
        return True, f"Đã gọi {khach.ma_khach()} - {khach.ten}", khach

    def hoan_thanh_phuc_vu(self, id_quay):
        quay = self._tim_quay(id_quay)
        if quay is None:
            return False, "Không tìm thấy quầy", None

        khach = quay.hoan_thanh_phuc_vu()
        if khach is None:
            return False, "Quầy chưa có khách đang phục vụ", None

        self.danh_sach_da_phuc_vu.append(khach)
        return True, f"Đã hoàn thành phục vụ {khach.ma_khach()} - {khach.ten}", khach

    def mo_quay(self, id_quay):
        quay = self._tim_quay(id_quay)
        if quay is None:
            return False, "Không tìm thấy quầy"
        quay.mo_quay()
        return True, f"Đã mở quầy {id_quay}"

    def dong_quay(self, id_quay):
        quay = self._tim_quay(id_quay)
        if quay is None:
            return False, "Không tìm thấy quầy"
        if not quay.dong_quay():
            return False, "Không thể đóng quầy đang phục vụ khách"
        return True, f"Đã đóng quầy {id_quay}"

    def lay_danh_sach_hang_doi_thuong(self):
        return self.hang_doi_thuong.to_list()

    def lay_danh_sach_hang_doi_uu_tien(self):
        return self.hang_doi_uu_tien.to_list()

    def lay_danh_sach_quay(self):
        return self.danh_sach_quay.copy()

    def lay_danh_sach_da_phuc_vu(self):
        return self.danh_sach_da_phuc_vu.copy()

    def tinh_thong_ke(self):
        tong_da_phuc_vu = len(self.danh_sach_da_phuc_vu)
        so_uu_tien_cho = self.hang_doi_uu_tien.size()
        so_thuong_cho = self.hang_doi_thuong.size()
        tong_dang_cho = so_uu_tien_cho + so_thuong_cho
        so_quay_mo = 0
        so_quay_ban = 0

        for quay in self.danh_sach_quay:
            if quay.dang_mo:
                so_quay_mo += 1
            if quay.khach_dang_phuc_vu is not None:
                so_quay_ban += 1

        thoi_gian_cho_tb = tinh_thoi_gian_cho_trung_binh(self.danh_sach_da_phuc_vu)
        khach_cho_lau_nhat = None
        for khach in self.danh_sach_da_phuc_vu:
            if khach_cho_lau_nhat is None or khach.tinh_thoi_gian_cho() > khach_cho_lau_nhat.tinh_thoi_gian_cho():
                khach_cho_lau_nhat = khach

        return {
            "tong_khach_da_phuc_vu": tong_da_phuc_vu,
            "tong_khach_dang_cho": tong_dang_cho,
            "so_khach_uu_tien_dang_cho": so_uu_tien_cho,
            "so_khach_thuong_dang_cho": so_thuong_cho,
            "so_quay_dang_mo": so_quay_mo,
            "so_quay_dang_ban": so_quay_ban,
            "thoi_gian_cho_trung_binh": thoi_gian_cho_tb,
            "khach_cho_lau_nhat": khach_cho_lau_nhat,
            "canh_bao": thoi_gian_cho_tb > 30,
        }

    def sap_xep_bao_cao_theo_thoi_gian_cho(self):
        return merge_sort_theo_thoi_gian_cho_giam_dan(self.danh_sach_da_phuc_vu)

    def _tim_quay(self, id_quay):
        for quay in self.danh_sach_quay:
            if quay.id_quay == id_quay:
                return quay
        return None
