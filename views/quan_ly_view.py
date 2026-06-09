import customtkinter as ctk

class QuanLyView:
    def __init__(self, root, app_context):
        self.root = root
        self.app_context = app_context

        self.frame = ctk.CTkFrame(self.root, corner_radius=0)

        user = self.app_context.get_current_user()

        self.title_label = ctk.CTkLabel(
            self.frame,
            text="🏦  GIAO DIỆN QUẢN LÝ",
            font=("Segoe UI", 28, "bold")
        )

        self.welcome_label = ctk.CTkLabel(
            self.frame,
            text=f"Xin chào Admin: {user.username}",
            font=("Segoe UI", 15)
        )

        self.logout_button = ctk.CTkButton(
            self.frame,
            text="Đăng xuất",
            width=160,
            height=38,
            fg_color="red",
            hover_color="#cc0000",
            font=("Segoe UI", 13, "bold"),
            command=self.dang_xuat
        )

    def show(self):
        self.frame.pack(fill="both", expand=True)
        self.title_label.pack(pady=(40, 10))
        self.welcome_label.pack(pady=(0, 20))
        self.logout_button.pack(pady=10)

    def hide(self):
        self.frame.pack_forget()

    def dang_xuat(self):
        self.app_context.set_current_user(None)
        self.hide()
        from views.login_view import LoginView
        LoginView(self.root, self.app_context).show()