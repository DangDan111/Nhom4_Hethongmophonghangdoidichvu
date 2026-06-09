class TaiKhoan:
    def __init__(self, username, password, role, quay_id=None):
        self.username = username
        self.password = password
        self.role = role
        self.quay_id = quay_id