import customtkinter as ctk
from services.auth_service import AuthService


class LoginView:
    def __init__(self, root, app_context):
        self.root = root
        self.app_context = app_context
        self.auth_service = AuthService()

        self.frame = ctk.CTkFrame(self.root, corner_radius=24)

        self.logo_label = ctk.CTkLabel(
            self.frame,
            text="🏦",
            font=("Segoe UI Emoji", 46)
        )

        self.title_label = ctk.CTkLabel(
            self.frame,
            text="ĐĂNG NHẬP",
            font=("Segoe UI", 32, "bold")
        )

        self.subtitle_label = ctk.CTkLabel(
            self.frame,
            text="Hệ thống quản lý ngân hàng",
            font=("Segoe UI", 16)
        )

        self.username_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="👤  Tên đăng nhập",
            width=320,
            height=44,
            font=("Segoe UI", 14)
        )

        self.password_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="🔒  Mật khẩu",
            show="*",
            width=320,
            height=44,
            font=("Segoe UI", 14)
        )

        self.show_password_checkbox = ctk.CTkCheckBox(
            self.frame,
            text="Hiển thị mật khẩu",
            font=("Segoe UI", 13),
            command=self.toggle_password
        )

        self.error_label = ctk.CTkLabel(
            self.frame,
            text="",
            text_color="red",
            font=("Segoe UI", 13)
        )

        self.login_button = ctk.CTkButton(
            self.frame,
            text="ĐĂNG NHẬP",
            width=320,
            height=44,
            font=("Segoe UI", 15, "bold"),
            command=self.handle_login
        )

        # Nhấn Enter để đăng nhập
        self.root.bind("<Return>", lambda event: self.handle_login())

    def show(self):
        self.frame.pack(
            padx=270,
            pady=45,
            fill="both",
            expand=True
        )

        self.logo_label.pack(pady=(35, 5))
        self.title_label.pack(pady=(0, 8))
        self.subtitle_label.pack(pady=(0, 30))

        self.username_entry.pack(pady=(0, 14))
        self.password_entry.pack(pady=(0, 8))

        self.show_password_checkbox.pack(
            anchor="w",
            padx=85,
            pady=(0, 15)
        )

        self.error_label.pack(pady=(0, 10))
        self.login_button.pack(pady=(0, 20))

    def hide(self):
        self.frame.pack_forget()

    def toggle_password(self):
        if self.show_password_checkbox.get() == 1:
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "":
            self.error_label.configure(text="Vui lòng nhập tên đăng nhập!")
            return

        if password == "":
            self.error_label.configure(text="Vui lòng nhập mật khẩu!")
            return

        result = self.auth_service.login(username, password)

        if result is None:
            self.error_label.configure(text="Sai tài khoản hoặc mật khẩu!")
            return

        self.error_label.configure(text="")
        self.app_context.set_current_user(result)

        print("Đăng nhập thành công")
        print("Username:", result.username)
        print("Role:", result.role)
        print("Quầy:", result.quay_id)