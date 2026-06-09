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

        self.root.bind("<Return>", lambda event: self.handle_login())

    def show(self):
        self.frame.pack(padx=270, pady=45, fill="both", expand=True)
        self.logo_label.pack(pady=(35, 5))
        self.title_label.pack(pady=(0, 8))
        self.subtitle_label.pack(pady=(0, 30))
        self.username_entry.pack(pady=(0, 14))
        self.password_entry.pack(pady=(0, 8))
        self.show_password_checkbox.pack(anchor="w", padx=85, pady=(0, 15))
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

        tai_khoan, thong_bao = self.auth_service.dang_nhap(username, password)

        if tai_khoan is None:
            self.error_label.configure(text=thong_bao)
            return

        self.error_label.configure(text="")
        self.app_context.set_current_user(tai_khoan)
        self.hide()

        role = tai_khoan.role

        if role == "quan_ly":
            from views.quan_ly_view import QuanLyView
            QuanLyView(self.root, self.app_context).show()

        elif role == "tiep_nhan":
            from views.tiep_nhan_view import TiepNhanView
            TiepNhanView(self.root, self.app_context).show()

        elif role == "nhan_vien_quay":
            from views.nhan_vien_quay_view import NhanVienQuayView
            NhanVienQuayView(self.root, self.app_context).show()