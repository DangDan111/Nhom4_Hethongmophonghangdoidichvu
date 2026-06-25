from services.he_thong_hang_doi import HeThongHangDoi


class DataStore:
    def __init__(self):
        # Hệ thống hàng đợi dùng chung
        self.he_thong = HeThongHangDoi(nap_du_lieu_mau=True)

        # Người dùng đang đăng nhập
        self.current_user = None

        # Nhật ký thao tác
        self.logs = []

        # Thông báo hệ thống
        self.notifications = []

    # ======================
    # Hệ thống hàng đợi
    # ======================
    def get_he_thong(self):
        return self.he_thong

    # ======================
    # User
    # ======================
    def set_current_user(self, user):
        self.current_user = user

    def get_current_user(self):
        return self.current_user

    # ======================
    # Log
    # ======================
    def add_log(self, message):
        self.logs.append(message)

    def get_logs(self):
        return self.logs

    # ======================
    # Notification
    # ======================
    def add_notification(self, text):
        self.notifications.append(text)

    def get_notifications(self):
        return self.notifications


# Singleton
data_store = DataStore()