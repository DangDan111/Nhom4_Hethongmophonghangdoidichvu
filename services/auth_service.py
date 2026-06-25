from models.tai_khoan import TaiKhoan


class AuthService:
    def __init__(self):
        self.danh_sach_tai_khoan = [
            TaiKhoan("admin", "123", "quan_ly"),
            TaiKhoan("tiepnhan", "123", "tiep_nhan"),
            TaiKhoan("quay1", "123", "nhan_vien_quay", quay_id=1),
            TaiKhoan("quay2", "123", "nhan_vien_quay", quay_id=2),
            TaiKhoan("quay3", "123", "nhan_vien_quay", quay_id=3),
        ]

    def dang_nhap(self, username, password):
        username = username.strip()
        password = password.strip()

        if username == "":
            return None, "Vui lòng nhập tên đăng nhập"
        if password == "":
            return None, "Vui lòng nhập mật khẩu"

        for tai_khoan in self.danh_sach_tai_khoan:
            if tai_khoan.username == username:
                if tai_khoan.password == password:
                    return tai_khoan, "Đăng nhập thành công"
                return None, "Mật khẩu không đúng"

        return None, "Tài khoản không tồn tại"
