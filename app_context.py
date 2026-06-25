from services.he_thong_hang_doi import HeThongHangDoi


class AppContext:
    def __init__(self, root=None):
        self.root = root
        self.current_user = None
        self.he_thong_hang_doi = HeThongHangDoi()
        self.he_thong_hang_doi.nap_du_lieu_mau()

    def set_current_user(self, user):
        self.current_user = user

    def get_current_user(self):
        return self.current_user

    def get_he_thong_hang_doi(self):
        return self.he_thong_hang_doi