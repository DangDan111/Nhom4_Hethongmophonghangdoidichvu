from datetime import datetime, timedelta

from models.khach_hang import KhachHang
from models.quay_giao_dich import QuayGiaoDich
from data_structures.linear_queue import LinearQueue
from data_structures.priority_queue_heap import PriorityQueueHeap
from utils.statistics import (
    merge_sort_theo_hai_long_giam_dan,
    merge_sort_theo_so_tien_giam_dan,
    merge_sort_theo_thoi_gian_cho_giam_dan,
    tinh_do_hai_long_trung_binh,
    tinh_thoi_gian_cho_trung_binh,
    tinh_tong_tien_giao_dich,
)


class HeThongHangDoi:
    def __init__(self):
        self.hang_doi_thuong = LinearQueue(max_size=50)
        self.hang_doi_uu_tien = PriorityQueueHeap(max_size=20)
        self.danh_sach_quay = []
        self.danh_sach_da_phuc_vu = []
        self.next_customer_id = 1

        for id_quay in range(1, 4):
            self.danh_sach_quay.append(QuayGiaoDich(id_quay, dang_mo=True))

    def nap_du_lieu_mau(self):
        if (
            self.hang_doi_thuong.size() > 0
            or self.hang_doi_uu_tien.size() > 0
            or len(self.danh_sach_da_phuc_vu) > 0
            or any(quay.khach_dang_phuc_vu is not None for quay in self.danh_sach_quay)
        ):
            return

        now = datetime.now()

        khach_dang_phuc_vu = [
            KhachHang(1, "Nguyễn Văn An", "Giao dịch nhanh", 5, thoi_gian_den=now - timedelta(minutes=18)),
            KhachHang(2, "Trần Thị Mai", "Giao dịch phức tạp", 5, thoi_gian_den=now - timedelta(minutes=15)),
            KhachHang(3, "Lê Quốc Huy", "Tư vấn dịch vụ", 5, thoi_gian_den=now - timedelta(minutes=12)),
        ]

        for quay, khach in zip(self.danh_sach_quay, khach_dang_phuc_vu):
            quay.tiep_nhan_khach(khach)

        khach_uu_tien = [
            KhachHang(4, "Phạm Thanh Hà", "VIP", 1, thoi_gian_den=now - timedelta(minutes=8)),
            KhachHang(5, "Đỗ Gia Hân", "Khẩn cấp", 2, thoi_gian_den=now - timedelta(minutes=7)),
            KhachHang(6, "Võ Minh Khang", "Người cao tuổi", 3, thoi_gian_den=now - timedelta(minutes=6)),
        ]
        for khach in khach_uu_tien:
            self.hang_doi_uu_tien.push(khach)

        khach_thuong = [
            KhachHang(7, "Bùi Ngọc Lan", "Giao dịch nhanh", 5, thoi_gian_den=now - timedelta(minutes=5)),
            KhachHang(8, "Hoàng Đức Minh", "Giao dịch phức tạp", 5, thoi_gian_den=now - timedelta(minutes=4)),
            KhachHang(9, "Ngô Thùy Dương", "Tư vấn dịch vụ", 5, thoi_gian_den=now - timedelta(minutes=3)),
            KhachHang(10, "Đặng Hải Yến", "Giao dịch nhanh", 5, thoi_gian_den=now - timedelta(minutes=2)),
        ]
        for khach in khach_thuong:
            self.hang_doi_thuong.enqueue(khach)

        khach_da_phuc_vu = [
            KhachHang(
                11,
                "Nguyễn Hoàng Nam",
                "Giao dịch nhanh",
                5,
                thoi_gian_den=now - timedelta(minutes=45),
                thoi_gian_bat_dau_phuc_vu=now - timedelta(minutes=32),
                thoi_gian_ket_thuc=now - timedelta(minutes=24),
                trang_thai="Đã phục vụ",
                so_tien_giao_dich=80000,
                muc_do_hai_long=8,
            ),
            KhachHang(
                12,
                "Phan Mỹ Linh",
                "VIP",
                1,
                thoi_gian_den=now - timedelta(minutes=38),
                thoi_gian_bat_dau_phuc_vu=now - timedelta(minutes=30),
                thoi_gian_ket_thuc=now - timedelta(minutes=18),
                trang_thai="Đã phục vụ",
                so_tien_giao_dich=430000,
                muc_do_hai_long=10,
            ),
        ]
        self.danh_sach_da_phuc_vu.extend(khach_da_phuc_vu)
        self.next_customer_id = 13

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
            so_tien_giao_dich=self._uoc_tinh_so_tien(loai_dich_vu, muc_do_uu_tien),
            muc_do_hai_long=self._uoc_tinh_hai_long(muc_do_uu_tien),
        )

        if muc_do_uu_tien < 5:
            if not self.hang_doi_uu_tien.push(khach):
                return False, "Hàng đợi ưu tiên đã đầy", None
            self.next_customer_id += 1
            return True, f"Đã thêm {khach.ma_khach()} vào hàng đợi ưu tiên", khach

        if not self.hang_doi_thuong.enqueue(khach):
            return False, "Hàng đợi thường đã đầy", None
        self.next_customer_id += 1
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

    def tu_dong_goi_khach_cho_quay_ranh(self):
        ket_qua = []
        for quay in self.danh_sach_quay:
            if quay.co_the_nhan_khach():
                ok, msg, khach = self.goi_khach_tiep_theo(quay.id_quay)
                if ok:
                    ket_qua.append((quay.id_quay, khach))
        return ket_qua

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
            "do_hai_long_trung_binh": tinh_do_hai_long_trung_binh(self.danh_sach_da_phuc_vu),
            "tong_tien_giao_dich": tinh_tong_tien_giao_dich(self.danh_sach_da_phuc_vu),
            "khach_cho_lau_nhat": khach_cho_lau_nhat,
            "canh_bao": thoi_gian_cho_tb > 30,
            "goi_y": "Cần thêm quầy" if thoi_gian_cho_tb > 30 else "Vận hành ổn định",
        }

    def sap_xep_bao_cao_theo_thoi_gian_cho(self):
        return merge_sort_theo_thoi_gian_cho_giam_dan(self.danh_sach_da_phuc_vu)

    def sap_xep_bao_cao_theo_so_tien(self):
        return merge_sort_theo_so_tien_giam_dan(self.danh_sach_da_phuc_vu)

    def sap_xep_bao_cao_theo_hai_long(self):
        return merge_sort_theo_hai_long_giam_dan(self.danh_sach_da_phuc_vu)

    def _tim_quay(self, id_quay):
        for quay in self.danh_sach_quay:
            if quay.id_quay == id_quay:
                return quay
        return None

    def _uoc_tinh_so_tien(self, loai_dich_vu, muc_do_uu_tien):
        bang_gia = {
            "Giao dịch nhanh": 80000,
            "Giao dịch phức tạp": 250000,
            "Tư vấn dịch vụ": 120000,
            "VIP": 350000,
            "Khẩn cấp": 500000,
            "Người cao tuổi": 90000,
        }
        return bang_gia.get(loai_dich_vu, 100000) + max(0, 5 - muc_do_uu_tien) * 20000

    def _uoc_tinh_hai_long(self, muc_do_uu_tien):
        diem = 6 + max(0, 5 - muc_do_uu_tien)
        return min(10, diem)
