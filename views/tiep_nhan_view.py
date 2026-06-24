import customtkinter as ctk
from tkinter import messagebox


class TiepNhanView:
    def __init__(self, root, app_context):
        self.root = root
        self.app_context = app_context
        self.user = app_context.get_current_user()
        self.he_thong = app_context.get_he_thong_hang_doi()
        self.frame = None
        self.service_options = {
            "Khám tổng quát - Thường": ("Khám tổng quát", 5),
            "Khám da liễu - Thường": ("Khám da liễu", 5),
            "Khám mắt - Thường": ("Khám mắt", 5),
            "VIP - Ưu tiên": ("VIP", 1),
            "Cấp cứu - Ưu tiên": ("Cấp cứu", 2),
            "Người cao tuổi - Ưu tiên": ("Người cao tuổi", 3),
        }

    def show(self):
        self._clear_root()
        self.root.title("Tiếp nhận khách hàng")
        self.root.geometry("1520x820")
        self.root.resizable(False, False)

        self.frame = ctk.CTkFrame(self.root, fg_color="#f5f8ff", corner_radius=0)
        self.frame.pack(fill="both", expand=True)

        header = ctk.CTkFrame(self.frame, height=92, fg_color="white", corner_radius=0, border_width=1, border_color="#d9e2f2")
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="GIAO DIỆN TIẾP NHẬN", font=("Segoe UI", 26, "bold"), text_color="#0f5bd7").place(x=40, y=20)
        ctk.CTkLabel(header, text="Thêm khách vào hàng đợi dịch vụ", font=("Segoe UI", 15), text_color="#4b5563").place(x=42, y=56)
        ctk.CTkLabel(header, text=f"Tài khoản: {self.user.username}", font=("Segoe UI", 14, "bold"), text_color="#111827").place(x=1190, y=34)
        ctk.CTkButton(header, text="Đăng xuất", width=135, height=38, font=("Segoe UI", 14, "bold"), fg_color="white", text_color="#0f5bd7", border_width=1, border_color="#0f5bd7", hover_color="#eef4ff", command=self.dang_xuat).place(x=1340, y=27)

        body = ctk.CTkFrame(self.frame, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=28, pady=24)
        body.grid_columnconfigure(0, weight=0)
        body.grid_columnconfigure(1, weight=1)

        form = ctk.CTkFrame(body, width=470, fg_color="white", corner_radius=10, border_width=1, border_color="#d9e2f2")
        form.grid(row=0, column=0, sticky="ns", padx=(0, 18))
        form.grid_propagate(False)

        ctk.CTkLabel(form, text="Thông tin khách hàng", font=("Segoe UI", 20, "bold"), text_color="#0f5bd7").pack(anchor="w", padx=24, pady=(24, 16))
        ctk.CTkLabel(form, text="Tên khách hàng", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=24)
        self.ten_entry = ctk.CTkEntry(form, width=420, height=44, placeholder_text="Nhập họ tên khách hàng", font=("Segoe UI", 14))
        self.ten_entry.pack(padx=24, pady=(8, 18))

        ctk.CTkLabel(form, text="Loại dịch vụ", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=24)
        self.loai_option = ctk.CTkOptionMenu(form, width=420, height=44, values=list(self.service_options.keys()), font=("Segoe UI", 14))
        self.loai_option.set("Khám tổng quát - Thường")
        self.loai_option.pack(padx=24, pady=(8, 22))

        ctk.CTkButton(form, text="Thêm vào hàng đợi", height=44, width=420, font=("Segoe UI", 14, "bold"), fg_color="#16a34a", hover_color="#15803d", command=self.them_khach).pack(padx=24, pady=(0, 14))
        ctk.CTkButton(form, text="Làm mới danh sách", height=40, width=420, font=("Segoe UI", 13, "bold"), fg_color="#0f5bd7", command=self.cap_nhat).pack(padx=24)

        summary = ctk.CTkFrame(form, fg_color="#eef6ff", corner_radius=8)
        summary.pack(fill="x", padx=24, pady=24)
        self.count_label = ctk.CTkLabel(summary, text="", font=("Segoe UI", 18, "bold"), text_color="#0f5bd7")
        self.count_label.pack(pady=16)

        monitor = ctk.CTkFrame(body, fg_color="white", corner_radius=10, border_width=1, border_color="#d9e2f2")
        monitor.grid(row=0, column=1, sticky="nsew")
        monitor.grid_rowconfigure(1, weight=1)
        monitor.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(monitor, text="Theo dõi hàng đợi", font=("Segoe UI", 20, "bold"), text_color="#0f5bd7").grid(row=0, column=0, sticky="w", padx=24, pady=(22, 10))
        self.monitor_text = ctk.CTkTextbox(monitor, font=("Consolas", 13), fg_color="#fbfdff", text_color="#111827")
        self.monitor_text.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 24))
        self.cap_nhat()

    def them_khach(self):
        ten = self.ten_entry.get().strip()
        loai_dich_vu, muc_do_uu_tien = self.service_options[self.loai_option.get()]
        ok, thong_bao, khach = self.he_thong.them_khach(ten, loai_dich_vu, muc_do_uu_tien)
        if not ok:
            messagebox.showwarning("Cảnh báo", thong_bao)
            return
        self.ten_entry.delete(0, "end")
        messagebox.showinfo("Thành công", thong_bao)
        self.cap_nhat()

    def cap_nhat(self):
        thong_ke = self.he_thong.tinh_thong_ke()
        self.count_label.configure(text=f"Khách đang chờ: {thong_ke['tong_khach_dang_cho']}")
        lines = []
        lines.append("HÀNG ĐỢI ƯU TIÊN")
        lines.append(self._format_khach_list(self.he_thong.lay_danh_sach_hang_doi_uu_tien()))
        lines.append("")
        lines.append("HÀNG ĐỢI THƯỜNG")
        lines.append(self._format_khach_list(self.he_thong.lay_danh_sach_hang_doi_thuong()))
        self._set_text("\n".join(lines))

    def _format_khach_list(self, ds_khach):
        if len(ds_khach) == 0:
            return "  Chưa có khách đang chờ."
        lines = ["  Mã KH   Tên khách                 Dịch vụ              Ưu tiên   Thời gian đến"]
        for khach in ds_khach:
            lines.append(f"  {khach.ma_khach():<7} {khach.ten:<24} {khach.loai_dich_vu:<20} {khach.muc_do_uu_tien:<8} {khach.thoi_gian_den.strftime('%H:%M:%S')}")
        return "\n".join(lines)

    def _set_text(self, text):
        self.monitor_text.configure(state="normal")
        self.monitor_text.delete("1.0", "end")
        self.monitor_text.insert("1.0", text)
        self.monitor_text.configure(state="disabled")

    def dang_xuat(self):
        self.app_context.set_current_user(None)
        from views.login_view import LoginView
        LoginView(self.root, self.app_context).show()

    def _clear_root(self):
        self.root.unbind("<Return>")
        for widget in self.root.winfo_children():
            widget.destroy()
