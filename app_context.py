from services.data_store import data_store


class AppContext:
    def __init__(self, root=None):
        self.root = root
        self.current_user = None

        # Lấy hệ thống dùng chung từ DataStore
        self.he_thong = data_store.get_he_thong()

    def set_current_user(self, user):
        self.current_user = user
        data_store.set_current_user(user)

    def get_current_user(self):
        return data_store.get_current_user()

    def get_he_thong_hang_doi(self):
        return self.he_thong