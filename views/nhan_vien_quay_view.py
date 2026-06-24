import customtkinter as ctk
from tkinter import messagebox


class NhanVienQuayView:
    def __init__(self, root, app_context):
        self.root = root
        self.app_context = app_context
        self.user = app_context.get_current_user()
        self.he_thong = app_context.get_he_thong_hang_doi()
        self.quay_id = self.user.quay_id or 1
        self.frame = None

    def show(self):
        self._clear_root()
        self.root.title(f"Nhân viên quầy {self.quay_id}")
        self.root.geometry("1520x820")
        self.root.resizable(False, False)

        self.frame = ctk.CTkFrame(self.root, fg_color="#f5f8ff", corner_radius=0)
        self.frame.pack(fill="both", expand=True)

        header = ctk.CTkFrame(self.frame, height=92, fg_color="white", corner_radius=0, border_width=1, border_color="#d9e2f2")
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="GIAO DIỆN NHÂN VIÊN QUẦY", font=("Segoe UI", 26, "bold"), text_color="#0f5bd7").place(x=40, y=20)
        ctk.CTkLabel(header, text=f"Quầy {self.quay_id} - gọi khách và hoàn thành phục vụ", font=("Segoe UI", 15), text_color="#4b5563").place(x=42, y=56)
        ctk.CTkLabel(header, text=f"Tài khoản: {self.user.username}", font=("Segoe UI", 14, "bold"), text_color="#111827").place(x=1190, y=34)
        ctk.CTkButton(header, text="Đăng xuất", width=135, height=38, font=("Segoe UI", 14, "bold"), fg_color="white", text_color="#0f5bd7", border_width=1, border_color="#0f5bd7", hover_color="#eef4ff", command=self.dang_xuat).place(x=1340, y=27)

        body = ctk.CTkFrame(self.frame, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=28, pady=24)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(body, fg_color="white", corner_radius=10, border_width=1, border_color="#d9e2f2")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        right = ctk.CTkFrame(body, fg_color="white", corner_radius=10, border_width=1, border_color="#d9e2f2")
        right.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        ctk.CTkLabel(left, text=f"Quầy {self.quay_id}", font=("Segoe UI", 24, "bold"), text_color="#0f5bd7").pack(anchor="w", padx=24, pady=(24, 8))
        self.status_label = ctk.CTkLabel(left, text="", font=("Segoe UI", 16, "bold"), text_color="#111827")
        self.status_label.pack(anchor="w", padx=24, pady=(0, 18))

        ctk.CTkButton(left, text="Gọi khách tiếp theo", width=300, height=46, font=("Segoe UI", 15, "bold"), fg_color="#0f5bd7", command=self.goi_khach).pack(anchor="w", padx=24, pady=(0, 14))
        ctk.CTkButton(left, text="Hoàn thành dịch vụ", width=300, height=46, font=("Segoe UI", 15, "bold"), fg_color="#16a34a", hover_color="#15803d", command=self.hoan_thanh).pack(anchor="w", padx=24, pady=(0, 20))

        ctk.CTkLabel(left, text="Khách đang phục vụ", font=("Segoe UI", 20, "bold"), text_color="#0f5bd7").pack(anchor="w", padx=24, pady=(12, 8))
        self.customer_text = ctk.CTkTextbox(left, height=300, font=("Consolas", 14), fg_color="#fbfdff", text_color="#111827")
        self.customer_text.pack(fill="x", padx=24, pady=(0, 24))

        ctk.CTkLabel(right, text="Lịch sử phục vụ của quầy", font=("Segoe UI", 20, "bold"), text_color="#0f5bd7").pack(anchor="w", padx=24, pady=(24, 10))
        self.history_text = ctk.CTkTextbox(right, font=("Consolas", 13), fg_color="#fbfdff", text_color="#111827")
        self.history_text.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        self.cap_nhat()

    def goi_khach(self):
        ok, thong_bao, khach = self.he_thong.goi_khach_tiep_theo(self.quay_id)
        if not ok:
            messagebox.showwarning("Thông báo", thong_bao)
        else:
            messagebox.showinfo("Thành công", thong_bao)
        self.cap_nhat()

    def hoan_thanh(self):
        ok, thong_bao, khach = self.he_thong.hoan_thanh_phuc_vu(self.quay_id)
        if not ok:
            messagebox.showwarning("Thông báo", thong_bao)
        else:
            messagebox.showinfo("Thành công", thong_bao)
        self.cap_nhat()

    def cap_nhat(self):
        quay = None
        for item in self.he_thong.lay_danh_sach_quay():
            if item.id_quay == self.quay_id:
                quay = item
                break

        if quay is None:
            return

        mo_dong = "Đang mở" if quay.dang_mo else "Đang đóng"
        self.status_label.configure(text=f"Trạng thái: {mo_dong} - {quay.trang_thai}")

        khach = quay.khach_dang_phuc_vu
        if khach is None:
            customer = "Hiện chưa có khách hàng nào đang phục vụ."
        else:
            customer = (
                f"Mã khách: {khach.ma_khach()}\n"
                f"Tên khách: {khach.ten}\n"
                f"Loại dịch vụ: {khach.loai_dich_vu}\n"
                f"Mức ưu tiên: {khach.muc_do_uu_tien}\n"
                f"Thời gian đến: {khach.thoi_gian_den.strftime('%H:%M:%S')}\n"
                f"Bắt đầu phục vụ: {khach.thoi_gian_bat_dau_phuc_vu.strftime('%H:%M:%S')}"
            )
        self._set_text(self.customer_text, customer)

        if len(quay.lich_su_phuc_vu) == 0:
            history = "Chưa có khách nào hoàn thành tại quầy này."
        else:
            lines = ["Mã KH   Tên khách                 Dịch vụ              Chờ(phút)  Phục vụ(phút)"]
            for khach in quay.lich_su_phuc_vu:
                lines.append(f"{khach.ma_khach():<7} {khach.ten:<24} {khach.loai_dich_vu:<20} {khach.tinh_thoi_gian_cho():<9.1f} {khach.tinh_thoi_gian_phuc_vu():.1f}")
            history = "\n".join(lines)
        self._set_text(self.history_text, history)

    def _set_text(self, textbox, text):
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")

    def dang_xuat(self):
        self.app_context.set_current_user(None)
        from views.login_view import LoginView
        LoginView(self.root, self.app_context).show()

    def _clear_root(self):
        self.root.unbind("<Return>")
        for widget in self.root.winfo_children():
            widget.destroy()
