def test_object_mau():
    print("=== TEST TẠO OBJECT MẪU ===")

    khach = {
        "ma": "KH001",
        "ten": "Nguyễn Văn A",
        "loai": "VIP",
        "uu_tien": 2
    }

    print(khach)


def test_fifo():
    print("\n=== TEST FIFO ===")

    queue = []

    queue.append("KH001")
    queue.append("KH002")
    queue.append("KH003")

    print(queue.pop(0))
    print(queue.pop(0))
    print(queue.pop(0))


def test_vip():
    print("\n=== TEST VIP ĐƯỢC GỌI TRƯỚC ===")

    khach_hang = [
        {"ma": "KH001", "loai": "Thuong", "uu_tien": 1},
        {"ma": "KH002", "loai": "VIP", "uu_tien": 2},
        {"ma": "KH003", "loai": "Thuong", "uu_tien": 1},
        {"ma": "KH004", "loai": "VIP", "uu_tien": 2},
    ]

    khach_hang.sort(key=lambda khach: khach["uu_tien"], reverse=True)

    for khach in khach_hang:
        print(khach["ma"], khach["loai"])


def test_nhap_lieu():
    print("\n=== TEST NHẬP LIỆU THÊM KHÁCH ===")

    ten = ""
    loai = "Thuong"

    if ten == "":
        print("Lỗi: Tên khách hàng không được bỏ trống")

    ten = "Trần Văn B"
    loai = ""

    if loai == "":
        print("Lỗi: Chưa chọn loại dịch vụ")

    sanh_cho = ["KH001", "KH002"]
    suc_chua = 2

    if len(sanh_cho) >= suc_chua:
        print("Lỗi: Sảnh chờ đã đầy")


def test_dong_quay():
    print("\n=== TEST ĐÓNG QUẦY ĐANG PHỤC VỤ ===")

    quay = {
        "ma_quay": "Quầy 1",
        "trang_thai": "DangPhucVu",
        "khach_dang_phuc_vu": "KH005"
    }

    if quay["trang_thai"] == "DangPhucVu":
        print("Không thể đóng quầy đang phục vụ")
    else:
        print("Đóng quầy thành công")


def test_hoan_thanh_dich_vu():
    print("\n=== TEST HOÀN THÀNH DỊCH VỤ ===")

    khach_dang_phuc_vu = "KH001"
    hang_cho = ["KH002", "KH003"]

    print("Hoàn thành:", khach_dang_phuc_vu)

    khach_dang_phuc_vu = None

    if len(hang_cho) > 0:
        khach_dang_phuc_vu = hang_cho.pop(0)
        print("Gọi khách tiếp theo:", khach_dang_phuc_vu)


def test_sort():
    print("\n=== TEST SORT THEO ƯU TIÊN ===")

    ds_khach = [
        {"ma": "KH001", "uu_tien": 1},
        {"ma": "KH002", "uu_tien": 3},
        {"ma": "KH003", "uu_tien": 2},
    ]

    ds_khach.sort(key=lambda khach: khach["uu_tien"], reverse=True)

    for khach in ds_khach:
        print(khach["ma"], "Ưu tiên:", khach["uu_tien"])


if __name__ == "__main__":
    test_object_mau()
    test_fifo()
    test_vip()
    test_nhap_lieu()
    test_dong_quay()
    test_hoan_thanh_dich_vu()
    test_sort()