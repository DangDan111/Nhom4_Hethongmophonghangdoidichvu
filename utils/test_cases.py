from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_structures.linear_queue import LinearQueue
from data_structures.priority_queue_heap import PriorityQueueHeap
from models.khach_hang import KhachHang
from services.he_thong_hang_doi import HeThongHangDoi
from utils.statistics import merge_sort_theo_thoi_gian_cho_giam_dan


def test_fifo():
    hang_doi = LinearQueue(max_size=3)
    hang_doi.enqueue("KH001")
    hang_doi.enqueue("KH002")
    hang_doi.enqueue("KH003")

    assert hang_doi.is_full()
    assert hang_doi.dequeue() == "KH001"
    assert hang_doi.dequeue() == "KH002"
    assert hang_doi.dequeue() == "KH003"
    assert hang_doi.dequeue() is None


def test_priority_queue_heap():
    hang_doi = PriorityQueueHeap(max_size=5)
    hang_doi.push(KhachHang(1, "Khách thường", "Giao dịch nhanh", 5))
    hang_doi.push(KhachHang(2, "Khách VIP", "VIP", 1))
    hang_doi.push(KhachHang(3, "Khách khẩn cấp", "Khẩn cấp", 2))

    assert hang_doi.pop().ten == "Khách VIP"
    assert hang_doi.pop().ten == "Khách khẩn cấp"
    assert hang_doi.pop().ten == "Khách thường"


def test_logic_uu_tien():
    he_thong = HeThongHangDoi()
    he_thong.them_khach("Nguyễn Văn A", "Giao dịch nhanh", 5)
    he_thong.them_khach("Trần Thị B", "VIP", 1)

    ok, _, khach = he_thong.goi_khach_tiep_theo(1)
    assert ok
    assert khach.ten == "Trần Thị B"

    ok, _, khach = he_thong.goi_khach_tiep_theo(2)
    assert ok
    assert khach.ten == "Nguyễn Văn A"


def test_du_lieu_mau():
    he_thong = HeThongHangDoi(nap_du_lieu_mau=True)
    tk = he_thong.tinh_thong_ke()

    assert tk["so_quay_dang_ban"] == 3
    assert tk["so_khach_uu_tien_dang_cho"] == 3
    assert tk["so_khach_thuong_dang_cho"] == 4
    assert he_thong.next_customer_id == 11


def test_overflow():
    hang_doi = LinearQueue(max_size=1)
    assert hang_doi.enqueue("KH001")
    assert not hang_doi.enqueue("KH002")

    uu_tien = PriorityQueueHeap(max_size=1)
    assert uu_tien.push(KhachHang(1, "A", "VIP", 1))
    assert not uu_tien.push(KhachHang(2, "B", "VIP", 1))


def test_merge_sort_theo_thoi_gian_cho():
    now = datetime.now()
    a = KhachHang(1, "A", "Thường", 5, thoi_gian_den=now - timedelta(minutes=5), thoi_gian_bat_dau_phuc_vu=now)
    b = KhachHang(2, "B", "Thường", 5, thoi_gian_den=now - timedelta(minutes=20), thoi_gian_bat_dau_phuc_vu=now)
    c = KhachHang(3, "C", "Thường", 5, thoi_gian_den=now - timedelta(minutes=10), thoi_gian_bat_dau_phuc_vu=now)

    ket_qua = merge_sort_theo_thoi_gian_cho_giam_dan([a, b, c])
    assert [khach.ten for khach in ket_qua] == ["B", "C", "A"]


def chay_tat_ca_test():
    test_fifo()
    test_priority_queue_heap()
    test_logic_uu_tien()
    test_du_lieu_mau()
    test_overflow()
    test_merge_sort_theo_thoi_gian_cho()
    print("Tất cả test đều đạt.")


if __name__ == "__main__":
    chay_tat_ca_test()
