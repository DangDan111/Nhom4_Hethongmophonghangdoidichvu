# Hệ thống mô phỏng hàng đợi dịch vụ

Đồ án mô phỏng quy trình tiếp nhận, xếp hàng và phục vụ khách hàng tại nhiều quầy giao dịch đa năng. Các quầy phục vụ cùng nhóm dịch vụ, vì vậy khách được đưa vào hàng đợi chung và quầy nào rảnh sẽ gọi khách tiếp theo theo đúng thứ tự ưu tiên.

## Chức năng chính

- Tiếp nhận khách hàng thường và khách hàng ưu tiên.
- Tự cài đặt hàng đợi thường theo cơ chế FIFO.
- Tự cài đặt hàng đợi ưu tiên bằng Heap, không dùng `queue.Queue` có sẵn.
- Nhân viên quầy gọi khách tiếp theo theo đúng thứ tự: ưu tiên trước, thường sau.
- Quản lý mở/đóng quầy và theo dõi trạng thái từng quầy.
- Thống kê số khách đã phục vụ, số khách còn chờ, số quầy đang mở, số quầy đang bận.
- Tính thời gian chờ trung bình, tổng tiền giao dịch và mức hài lòng trung bình.
- Cảnh báo cần thêm quầy khi thời gian chờ trung bình vượt 30 phút.
- Sắp xếp báo cáo bằng Merge Sort theo thời gian chờ, số tiền giao dịch hoặc mức độ hài lòng.

## Nhóm dịch vụ và mức ưu tiên

| Nhóm khách/dịch vụ | Mức ưu tiên |
| --- | ---: |
| VIP - Ưu tiên | 1 |
| Khẩn cấp - Ưu tiên | 2 |
| Người cao tuổi - Ưu tiên | 3 |
| Dự phòng mở rộng | 4 |
| Giao dịch nhanh / phức tạp / tư vấn dịch vụ | 5 |

Số ưu tiên càng nhỏ thì càng được phục vụ trước. Mức 4 được để dự phòng cho các nhóm có thể mở rộng sau này như khách đặt lịch trước hoặc hội viên. Nếu hai khách có cùng mức ưu tiên, hệ thống phục vụ theo thứ tự đến trước.

## Tài khoản mẫu

| Vai trò | Tài khoản | Mật khẩu |
| --- | --- | --- |
| Quản lý | admin | 123 |
| Tiếp nhận | tiepnhan | 123 |
| Nhân viên quầy 1 | quay1 | 123 |
| Nhân viên quầy 2 | quay2 | 123 |
| Nhân viên quầy 3 | quay3 | 123 |

## Cấu trúc chính

- `models/khach_hang.py`: lớp khách hàng.
- `models/quay_giao_dich.py`: lớp quầy giao dịch.
- `data_structures/linear_queue.py`: hàng đợi thường FIFO.
- `data_structures/priority_queue_heap.py`: hàng đợi ưu tiên bằng Heap.
- `services/he_thong_hang_doi.py`: nghiệp vụ mô phỏng hàng đợi.
- `utils/statistics.py`: thống kê và Merge Sort.
- `ui/`: giao diện thiết kế bằng Qt Designer.
- `views/`: code kết nối giao diện với nghiệp vụ.

## Chạy chương trình

```bash
python main.py
```

## Chạy kiểm thử nhanh

```bash
python utils/test_cases.py
```
