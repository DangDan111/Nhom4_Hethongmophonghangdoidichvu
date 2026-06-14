import customtkinter as ctk


class NhanVienQuayView:
    def __init__(self, root, username="quay1", on_logout_callback=None):
        self.root = root
        if hasattr(username, "current_user"):
            user = username.current_user
            self.username = user.username
        else:
            self.username = username
        self.on_logout_callback = on_logout_callback

        self.root.title("Giao diện Nhân viên quầy - Nhóm 4")
        self.root.geometry("650x550")
        self.root.resizable(False, False)

        self.init_components()

    def init_components(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # HEADER
        header_frame = ctk.CTkFrame(
            self.root,
            width=650,
            height=70,
            corner_radius=0,
            fg_color="#2f4054"
        )
        header_frame.place(x=0, y=0)

        title_label = ctk.CTkLabel(
            header_frame,
            text="GIAO DIỆN NHÂN VIÊN QUẦY",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        )
        title_label.place(x=20, y=22)

        account_label = ctk.CTkLabel(
            header_frame,
            text=f"Tài khoản: {self.username}",
            font=("Segoe UI", 13),
            text_color="white"
        )
        account_label.place(x=420, y=25)

        logout_btn = ctk.CTkButton(
            header_frame,
            text="Đăng xuất",
            width=95,
            height=35,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            font=("Segoe UI", 13, "bold"),
            command=self.logout
        )
        logout_btn.place(x=535, y=17)

        # FRAME THÔNG TIN QUẦY
        info_frame = ctk.CTkFrame(
            self.root,
            width=600,
            height=160,
            fg_color="#2b2b2b",
            corner_radius=8
        )
        info_frame.place(x=25, y=95)

        info_title = ctk.CTkLabel(
            info_frame,
            text="Thông tin quầy giao dịch",
            font=("Segoe UI", 17, "bold"),
            text_color="white"
        )
        info_title.place(x=20, y=18)

        quay_so = self.get_quay_so()

        quay_label = ctk.CTkLabel(
            info_frame,
            text=f"Mã quầy: Quầy {quay_so}",
            font=("Segoe UI", 14),
            text_color="white"
        )
        quay_label.place(x=20, y=65)

        status_label = ctk.CTkLabel(
            info_frame,
            text="Trạng thái: Rảnh",
            font=("Segoe UI", 14),
            text_color="white"
        )
        status_label.place(x=20, y=100)

        # FRAME KHÁCH ĐANG PHỤC VỤ
        customer_frame = ctk.CTkFrame(
            self.root,
            width=600,
            height=230,
            fg_color="#2b2b2b",
            corner_radius=8
        )
        customer_frame.place(x=25, y=280)

        customer_title = ctk.CTkLabel(
            customer_frame,
            text="Khách hàng đang phục vụ",
            font=("Segoe UI", 17, "bold"),
            text_color="white"
        )
        customer_title.place(x=20, y=18)

        self.customer_box = ctk.CTkTextbox(
            customer_frame,
            width=560,
            height=100,
            fg_color="#171c1c",
            text_color="white",
            font=("Segoe UI", 14)
        )
        self.customer_box.place(x=20, y=60)
        self.customer_box.insert("0.0", "Hiện chưa có khách hàng nào đang phục vụ.")
        self.customer_box.configure(state="disabled")

        complete_btn = ctk.CTkButton(
            customer_frame,
            text="Hoàn thành dịch vụ",
            width=180,
            height=40,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            font=("Segoe UI", 14, "bold")
        )
        complete_btn.place(x=20, y=175)

    def get_quay_so(self):
        if "1" in self.username:
            return "1"
        elif "2" in self.username:
            return "2"
        elif "3" in self.username:
            return "3"
        return "1"

    def logout(self):
        if self.on_logout_callback:
            self.on_logout_callback()
if __name__ == "__main__":
    import customtkinter as ctk

    root = ctk.CTk()

    app = NhanVienQuayView(
        root,
        username="quay1"
    )

    root.mainloop()