import customtkinter as ctk
from tkinter import messagebox


class QuanLyView:
    def __init__(self, root, app_context):
        self.root = root
        self.app_context = app_context
        self.user = app_context.get_current_user()
        self.he_thong = app_context.get_he_thong_hang_doi()
        self.frame = None
        self.bao_cao_da_sap_xep = False
        self.quay_option = None

    def show(self):
        self._clear_root()
        self.root.title("Hệ thống mô phỏng hàng đợi dịch vụ")
        self.root.geometry("1520x820")
        self.root.resizable(False, False)

        self.frame = ctk.CTkFrame(self.root, fg_color="#f5f8ff", corner_radius=0)
        self.frame.pack(fill="both", expand=True)

        self._tao_header()
        self._tao_noi_dung()
        self.lam_moi()

    def _tao_header(self):
        header = ctk.CTkFrame(self.frame, height=126, fg_color="white", corner_radius=0, border_width=1, border_color="#d9e2f2")
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="GIAO DIỆN QUẢN LÝ", font=("Segoe UI", 28, "bold"), text_color="#0f5bd7").place(x=46, y=28)
        ctk.CTkLabel(header, text="Hệ thống mô phỏng hàng đợi dịch vụ", font=("Segoe UI", 16), text_color="#4b5563").place(x=48, y=68)
        ctk.CTkLabel(header, text=f"Tài khoản: {self.user.username}", font=("Segoe UI", 15, "bold"), text_color="#111827").place(x=1190, y=45)
        ctk.CTkButton(header, text="Đăng xuất", width=140, height=40, font=("Segoe UI", 14, "bold"), fg_color="white", text_color="#0f5bd7", border_width=1, border_color="#0f5bd7", hover_color="#eef4ff", command=self.dang_xuat).place(x=1345, y=36)

    def _tao_noi_dung(self):
        content = ctk.CTkFrame(self.frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=16)

        stats = ctk.CTkFrame(content, fg_color="transparent")
        stats.pack(fill="x")
        self.stat_labels = {}
        cards = [
            ("tong", "Tổng khách đã phục vụ", "#0f5bd7"),
            ("cho", "Khách đang chờ", "#f59e0b"),
            ("mo", "Quầy đang mở", "#16a34a"),
            ("ban", "Quầy đang bận", "#6d42d8"),
            ("tb", "Thời gian chờ trung bình", "#0f5bd7"),
            ("canh_bao", "Cảnh báo", "#16a34a"),
        ]
        for index, (key, title, color) in enumerate(cards):
            stats.grid_columnconfigure(index, weight=1)
            card = ctk.CTkFrame(stats, height=96, fg_color="white", corner_radius=10, border_width=1, border_color="#d9e2f2")
            card.grid(row=0, column=index, sticky="ew", padx=6)
            card.pack_propagate(False)
            ctk.CTkLabel(card, text=title, font=("Segoe UI", 14), text_color="#111827").pack(anchor="w", padx=20, pady=(18, 0))
            self.stat_labels[key] = ctk.CTkLabel(card, text="0", font=("Segoe UI", 26, "bold"), text_color=color)
            self.stat_labels[key].pack(anchor="w", padx=20)

        middle = ctk.CTkFrame(content, fg_color="transparent")
        middle.pack(fill="x", pady=(16, 0))
        middle.grid_columnconfigure(0, weight=1)
        middle.grid_columnconfigure(1, weight=1)
        middle.grid_columnconfigure(2, weight=1)

        self.txt_uu_tien = self._tao_text_card(middle, 0, "Hàng đợi ưu tiên")
        self.txt_thuong = self._tao_text_card(middle, 1, "Hàng đợi thường")
        self.txt_quay = self._tao_quay_card(middle, 2)

        report = ctk.CTkFrame(content, fg_color="white", corner_radius=10, border_width=1, border_color="#d9e2f2")
        report.pack(fill="both", expand=True, pady=(16, 0))
        report.grid_columnconfigure(0, weight=1)
        report.grid_rowconfigure(1, weight=1)
        title_bar = ctk.CTkFrame(report, height=52, fg_color="white", corner_radius=10)
        title_bar.grid(row=0, column=0, sticky="ew")
        title_bar.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(title_bar, text="Báo cáo khách đã phục vụ", font=("Segoe UI", 18, "bold"), text_color="#0f5bd7").grid(row=0, column=0, sticky="w", padx=20, pady=12)
        ctk.CTkButton(title_bar, text="Sắp xếp theo thời gian chờ", height=34, width=220, font=("Segoe UI", 13, "bold"), fg_color="white", text_color="#0f5bd7", border_width=1, border_color="#d9e2f2", hover_color="#eef4ff", command=self.sap_xep_bao_cao).grid(row=0, column=1, padx=(0, 10))
        ctk.CTkButton(title_bar, text="Làm mới", height=34, width=105, font=("Segoe UI", 13, "bold"), fg_color="white", text_color="#0f5bd7", border_width=1, border_color="#d9e2f2", hover_color="#eef4ff", command=self.lam_moi).grid(row=0, column=2, padx=(0, 14))
        self.txt_bao_cao = ctk.CTkTextbox(report, font=("Consolas", 13), fg_color="#fbfdff", text_color="#111827")
        self.txt_bao_cao.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))

    def _tao_text_card(self, parent, col, title):
        card = ctk.CTkFrame(parent, height=260, fg_color="white", corner_radius=10, border_width=1, border_color="#d9e2f2")
        card.grid(row=0, column=col, sticky="nsew", padx=6)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 18, "bold"), text_color="#0f5bd7").grid(row=0, column=0, sticky="w", padx=18, pady=(16, 8))
        textbox = ctk.CTkTextbox(card, height=180, font=("Consolas", 12), fg_color="#fbfdff", text_color="#111827")
        textbox.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        return textbox

    def _tao_quay_card(self, parent, col):
        card = ctk.CTkFrame(parent, height=260, fg_color="white", corner_radius=10, border_width=1, border_color="#d9e2f2")
        card.grid(row=0, column=col, sticky="nsew", padx=6)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(card, text="Trạng thái quầy", font=("Segoe UI", 18, "bold"), text_color="#0f5bd7").grid(row=0, column=0, sticky="w", padx=18, pady=(16, 8))
        textbox = ctk.CTkTextbox(card, height=142, font=("Consolas", 12), fg_color="#fbfdff", text_color="#111827")
        textbox.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 8))

        controls = ctk.CTkFrame(card, fg_color="white")
        controls.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 12))
        self.quay_option = ctk.CTkOptionMenu(controls, values=["Quầy 1", "Quầy 2", "Quầy 3"], width=110, height=34, font=("Segoe UI", 13))
        self.quay_option.set("Quầy 1")
        self.quay_option.pack(side="left", padx=(0, 8))
        ctk.CTkButton(controls, text="Mở quầy", width=105, height=34, font=("Segoe UI", 13, "bold"), fg_color="#0f5bd7", command=self.mo_quay).pack(side="left", padx=4)
        ctk.CTkButton(controls, text="Đóng quầy", width=110, height=34, font=("Segoe UI", 13, "bold"), fg_color="#ef4444", hover_color="#dc2626", command=self.dong_quay).pack(side="left", padx=4)
        return textbox

    def lam_moi(self):
        thong_ke = self.he_thong.tinh_thong_ke()
        self.stat_labels["tong"].configure(text=str(thong_ke["tong_khach_da_phuc_vu"]))
        self.stat_labels["cho"].configure(text=str(thong_ke["tong_khach_dang_cho"]))
        self.stat_labels["mo"].configure(text=str(thong_ke["so_quay_dang_mo"]))
        self.stat_labels["ban"].configure(text=str(thong_ke["so_quay_dang_ban"]))
        self.stat_labels["tb"].configure(text=f"{thong_ke['thoi_gian_cho_trung_binh']:.1f} phút")
        self.stat_labels["canh_bao"].configure(text="Quá tải" if thong_ke["canh_bao"] else "Ổn định", text_color="#ef4444" if thong_ke["canh_bao"] else "#16a34a")

        self._set_text(self.txt_uu_tien, self._format_khach(self.he_thong.lay_danh_sach_hang_doi_uu_tien()))
        self._set_text(self.txt_thuong, self._format_khach(self.he_thong.lay_danh_sach_hang_doi_thuong()))
        self._set_text(self.txt_quay, self._format_quay())
        self._set_text(self.txt_bao_cao, self._format_bao_cao())

    def sap_xep_bao_cao(self):
        self.bao_cao_da_sap_xep = True
        self.lam_moi()

    def mo_quay(self):
        id_quay = self._lay_id_quay_dang_chon()
        ok, thong_bao = self.he_thong.mo_quay(id_quay)
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showwarning("Thông báo", thong_bao)
        self.lam_moi()

    def dong_quay(self):
        id_quay = self._lay_id_quay_dang_chon()
        ok, thong_bao = self.he_thong.dong_quay(id_quay)
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showwarning("Thông báo", thong_bao)
        self.lam_moi()

    def _lay_id_quay_dang_chon(self):
        return int(self.quay_option.get().replace("Quầy ", ""))

    def _format_khach(self, ds_khach):
        if len(ds_khach) == 0:
            return "Chưa có khách đang chờ."
        lines = ["Mã KH   Tên khách             Dịch vụ        Ưu tiên   Đến lúc"]
        for khach in ds_khach:
            lines.append(f"{khach.ma_khach():<7} {khach.ten:<20} {khach.loai_dich_vu:<14} {khach.muc_do_uu_tien:<8} {khach.thoi_gian_den.strftime('%H:%M:%S')}")
        return "\n".join(lines)

    def _format_quay(self):
        lines = ["Quầy   Mở/Đóng     Trạng thái       Khách"]
        for quay in self.he_thong.lay_danh_sach_quay():
            mo_dong = "Mở" if quay.dang_mo else "Đóng"
            khach = "-"
            if quay.khach_dang_phuc_vu is not None:
                khach = quay.khach_dang_phuc_vu.ma_khach()
            lines.append(f"{quay.id_quay:<6} {mo_dong:<11} {quay.trang_thai:<16} {khach}")
        return "\n".join(lines)

    def _format_bao_cao(self):
        ds = self.he_thong.sap_xep_bao_cao_theo_thoi_gian_cho() if self.bao_cao_da_sap_xep else self.he_thong.lay_danh_sach_da_phuc_vu()
        if len(ds) == 0:
            return "Chưa có khách đã phục vụ."
        lines = ["Mã KH   Tên khách                 Loại dịch vụ          Chờ(phút)  Phục vụ(phút)  Trạng thái"]
        for khach in ds:
            lines.append(f"{khach.ma_khach():<7} {khach.ten:<24} {khach.loai_dich_vu:<20} {khach.tinh_thoi_gian_cho():<9.1f} {khach.tinh_thoi_gian_phuc_vu():<13.1f} {khach.trang_thai}")
        return "\n".join(lines)

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
