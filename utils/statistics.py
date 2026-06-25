def merge_sort_theo_thoi_gian_cho_giam_dan(danh_sach):
    return merge_sort(danh_sach, lambda khach: khach.tinh_thoi_gian_cho(), giam_dan=True)


def merge_sort_theo_so_tien_giam_dan(danh_sach):
    return merge_sort(danh_sach, lambda khach: khach.so_tien_giao_dich, giam_dan=True)


def merge_sort_theo_hai_long_giam_dan(danh_sach):
    return merge_sort(danh_sach, lambda khach: khach.muc_do_hai_long, giam_dan=True)


def merge_sort(danh_sach, lay_gia_tri, giam_dan=True):
    if len(danh_sach) <= 1:
        return danh_sach.copy()

    mid = len(danh_sach) // 2
    trai = merge_sort(danh_sach[:mid], lay_gia_tri, giam_dan)
    phai = merge_sort(danh_sach[mid:], lay_gia_tri, giam_dan)
    return _merge(trai, phai, lay_gia_tri, giam_dan)


def _merge(trai, phai, lay_gia_tri, giam_dan):
    ket_qua = []
    i = 0
    j = 0

    while i < len(trai) and j < len(phai):
        gia_tri_trai = lay_gia_tri(trai[i])
        gia_tri_phai = lay_gia_tri(phai[j])
        dung_thu_tu = gia_tri_trai >= gia_tri_phai if giam_dan else gia_tri_trai <= gia_tri_phai

        if dung_thu_tu:
            ket_qua.append(trai[i])
            i += 1
        else:
            ket_qua.append(phai[j])
            j += 1

    while i < len(trai):
        ket_qua.append(trai[i])
        i += 1

    while j < len(phai):
        ket_qua.append(phai[j])
        j += 1

    return ket_qua


def tinh_thoi_gian_cho_trung_binh(danh_sach_da_phuc_vu):
    if len(danh_sach_da_phuc_vu) == 0:
        return 0

    tong = 0

    for khach in danh_sach_da_phuc_vu:
        tong += khach.tinh_thoi_gian_cho()

    # đổi sang phút
    return (tong / len(danh_sach_da_phuc_vu)) / 60


def tinh_do_hai_long_trung_binh(danh_sach_da_phuc_vu):
    if len(danh_sach_da_phuc_vu) == 0:
        return 0
    tong = 0
    for khach in danh_sach_da_phuc_vu:
        tong += khach.muc_do_hai_long
    return tong / len(danh_sach_da_phuc_vu)


def tinh_tong_tien_giao_dich(danh_sach_da_phuc_vu):
    tong = 0
    for khach in danh_sach_da_phuc_vu:
        tong += khach.so_tien_giao_dich
    return tong
