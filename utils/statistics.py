def merge_sort_theo_thoi_gian_cho_giam_dan(danh_sach):
    if len(danh_sach) <= 1:
        return danh_sach.copy()

    mid = len(danh_sach) // 2
    trai = merge_sort_theo_thoi_gian_cho_giam_dan(danh_sach[:mid])
    phai = merge_sort_theo_thoi_gian_cho_giam_dan(danh_sach[mid:])
    return _merge_giam_dan(trai, phai)


def _merge_giam_dan(trai, phai):
    ket_qua = []
    i = 0
    j = 0

    while i < len(trai) and j < len(phai):
        if trai[i].tinh_thoi_gian_cho() >= phai[j].tinh_thoi_gian_cho():
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
    return tong / len(danh_sach_da_phuc_vu)
