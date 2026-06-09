class AppContext:
    def __init__(self, root):
        self.root = root
        self.current_user = None

    def set_current_user(self, user):
        self.current_user = user

    def get_current_user(self):
        return self.current_user