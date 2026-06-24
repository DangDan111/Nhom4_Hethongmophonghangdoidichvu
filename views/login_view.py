import customtkinter as ctk

from services.auth_service import AuthService


class LoginView:
    def __init__(self, root, app_context):
        self.root = root
        self.app_context = app_context
        self.auth_service = AuthService()
        self.frame = None

    def show(self):
        self._clear_root()
        self.root.title("Hệ thống mô phỏng hàng đợi dịch vụ")
        self.root.geometry("1520x820")
        self.root.resizable(False, False)
        self.root.bind("<Return>", lambda event: self.handle_login())

        self.frame = ctk.CTkFrame(self.root, fg_color="#f5f8ff", corner_radius=0)
        self.frame.pack(fill="both", expand=True)

        card = ctk.CTkFrame(self.frame, width=480, height=520, fg_color="white", corner_radius=16, border_width=1, border_color="#d9e2f2")
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text="ĐĂNG NHẬP HỆ THỐNG", font=("Segoe UI", 28, "bold"), text_color="#0f5bd7").pack(pady=(50, 8))
        ctk.CTkLabel(card, text="Hệ thống mô phỏng hàng đợi dịch vụ", font=("Segoe UI", 15), text_color="#4b5563").pack(pady=(0, 32))

        self.username_entry = ctk.CTkEntry(card, width=350, height=44, placeholder_text="Tên đăng nhập", font=("Segoe UI", 14))
        self.username_entry.pack(pady=(0, 14))

        self.password_entry = ctk.CTkEntry(card, width=350, height=44, placeholder_text="Mật khẩu", show="*", font=("Segoe UI", 14))
        self.password_entry.pack(pady=(0, 10))

        self.show_password = ctk.CTkCheckBox(card, text="Hiển thị mật khẩu", font=("Segoe UI", 13), command=self.toggle_password)
        self.show_password.pack(anchor="w", padx=65, pady=(0, 16))

        self.error_label = ctk.CTkLabel(card, text="", font=("Segoe UI", 13), text_color="#dc2626")
        self.error_label.pack(pady=(0, 10))

        ctk.CTkButton(card, text="ĐĂNG NHẬP", width=350, height=44, font=("Segoe UI", 14, "bold"), command=self.handle_login).pack(pady=(0, 24))
        ctk.CTkLabel(card, text="Tài khoản mẫu: admin, tiepnhan, quay1, quay2, quay3 / mật khẩu 123", font=("Segoe UI", 12), text_color="#64748b", wraplength=360).pack()

        self.username_entry.focus()

    def toggle_password(self):
        self.password_entry.configure(show="" if self.show_password.get() == 1 else "*")

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        tai_khoan, thong_bao = self.auth_service.dang_nhap(username, password)

        if tai_khoan is None:
            self.error_label.configure(text=thong_bao)
            return

        self.app_context.set_current_user(tai_khoan)
        if tai_khoan.role == "quan_ly":
            from views.quan_ly_view import QuanLyView
            QuanLyView(self.root, self.app_context).show()
        elif tai_khoan.role == "tiep_nhan":
            from views.tiep_nhan_view import TiepNhanView
            TiepNhanView(self.root, self.app_context).show()
        elif tai_khoan.role == "nhan_vien_quay":
            from views.nhan_vien_quay_view import NhanVienQuayView
            NhanVienQuayView(self.root, self.app_context).show()

    def _clear_root(self):
        self.root.unbind("<Return>")
        for widget in self.root.winfo_children():
            widget.destroy()
