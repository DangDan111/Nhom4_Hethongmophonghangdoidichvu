import customtkinter as ctk
from tkinter import messagebox

# Thiết kế giao diện theo phong cách hiện đại (Dark/Light mode)
ctk.set_appearance_mode("System")  # Tự động theo giao diện máy tính (hoặc "Dark"/"Light")
ctk.set_default_color_theme("blue") # Tone màu xanh hiện đại

class TiepNhanView:
    def __init__(self, root, username="tiepnhan", on_logout_callback=None):
        self.root = root
        self.root.title("Giao diện Tiếp nhận - Nhóm 4")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        
        self.username = username
        self.on_logout_callback = on_logout_callback
        
        # Giao diện chính
        self.init_components()

    def init_components(self):
        # 1. Header hiển thị thông tin chung (Dùng CTKFrame)
        header_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="#2c3e50")
        header_frame.pack(fill=ctk.X, side=ctk.TOP)
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="GIAO DIỆN BỘ PHẬN TIẾP NHẬN", 
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"), 
            text_color="white"
        )
        title_label.pack(side=ctk.LEFT, padx=15, pady=15)
        
        # Nút Đăng xuất kiểu bo góc hiện đại
        btn_logout = ctk.CTkButton(
            header_frame, 
            text="Đăng xuất", 
            command=self.logout, 
            fg_color="#e74c3c", 
            hover_color="#c0392b",
            width=90,
            font=ctk.CTkFont(family="Arial", size=12, weight="bold")
        )
        btn_logout.pack(side=ctk.RIGHT, padx=15, pady=15)
        
        # Hiển thị tên tài khoản
        user_info = f"Tài khoản: {self.username}"
        user_label = ctk.CTkLabel(header_frame, text=user_info, text_color="white", font=ctk.CTkFont(family="Arial", size=12))
        user_label.pack(side=ctk.RIGHT, padx=5)

        # 2. KHUNG TIẾP NHẬN / THÊM KHÁCH HÀNG (Dùng CTKFrame làm hộp chứa)
        add_customer_frame = ctk.CTkFrame(self.root)
        add_customer_frame.pack(fill=ctk.X, padx=20, pady=20)
        
        # Tiêu đề nhóm nội bộ
        section_title = ctk.CTkLabel(add_customer_frame, text="Tiếp nhận Khách hàng mới", font=ctk.CTkFont(size=14, weight="bold"))
        section_title.grid(row=0, column=0, columnspan=2, sticky=ctk.W, padx=15, pady=(10, 5))
        
        # Nhập tên khách hàng (CTkEntry bo góc cực đẹp)
        ctk.CTkLabel(add_customer_frame, text="Họ và tên khách hàng:", font=ctk.CTkFont(size=13)).grid(row=1, column=0, sticky=ctk.W, padx=15, pady=10)
        self.ent_customer_name = ctk.CTkEntry(add_customer_frame, width=250, placeholder_text="Nhập tên khách hàng...")
        self.ent_customer_name.grid(row=1, column=1, padx=15, pady=10, sticky=ctk.E)
        
        # Chọn loại dịch vụ (Sử dụng CTkOptionMenu hiện đại thay cho Combobox cũ)
        ctk.CTkLabel(add_customer_frame, text="Loại dịch vụ:", font=ctk.CTkFont(size=13)).grid(row=2, column=0, sticky=ctk.W, padx=15, pady=10)
        self.cbo_service_type = ctk.CTkOptionMenu(
            add_customer_frame, 
            values=["Thường", "VIP (Ưu tiên)"],
            width=250
        )
        self.cbo_service_type.set("Thường") # Mặc định chọn dịch vụ Thường
        self.cbo_service_type.grid(row=2, column=1, padx=15, pady=10, sticky=ctk.E)
        
        # Nút thêm khách (CTkButton)
        self.btn_add_customer = ctk.CTkButton(
            add_customer_frame, 
            text="Thêm vào hàng đợi", 
            command=self.handle_add_customer,
            fg_color="#2ecc71", 
            hover_color="#27ae60",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=200
        )
        self.btn_add_customer.grid(row=3, column=0, columnspan=2, pady=(15, 15))

        # 3. KHUNG HIỂN THỊ TRẠNG THÁI HÀNG ĐỢI SƠ BỘ
        queue_info_frame = ctk.CTkFrame(self.root)
        queue_info_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Tiêu đề vùng hiển thị trạng thái
        queue_title = ctk.CTkLabel(queue_info_frame, text="Trạng thái hàng đợi hiện tại", font=ctk.CTkFont(size=14, weight="bold"))
        queue_title.pack(anchor=ctk.W, padx=15, pady=(10, 5))
        
        # Số lượng khách đang chờ
        self.lbl_queue_size = ctk.CTkLabel(queue_info_frame, text="Số lượng khách đang chờ: 0", font=ctk.CTkFont(size=12))
        self.lbl_queue_size.pack(anchor=ctk.W, padx=15, pady=2)
        
        # Khung text giám sát (Dùng CTkTextbox mượt mà hơn Text thường)
        self.txt_monitor = ctk.CTkTextbox(queue_info_frame, activate_scrollbars=True)
        self.txt_monitor.pack(fill=ctk.BOTH, expand=True, padx=15, pady=(5, 15))
        self.txt_monitor.configure(state="disabled")

    def handle_add_customer(self):
        """
        Hàm xử lý khi bấm nút Thêm khách.
        """
        name = self.ent_customer_name.get().strip()
        service = self.cbo_service_type.get()
        
        if not name:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên khách hàng!")
            return
            
        messagebox.showinfo("Thành công", f"Đã tiếp nhận khách hàng: {name} ({service})")
        
        # Xóa trắng ô nhập sau khi thêm thành công
        self.ent_customer_name.delete(0, ctk.END)

    def logout(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?"):
            if self.on_logout_callback:
                self.on_logout_callback()
            else:
                self.root.destroy()

# Chạy thử độc lập bằng CustomTkinter
if __name__ == "__main__":
    # Lưu ý: Khi dùng CustomTkinter chạy độc lập, root phải là ctk.CTk() chứ không phải tk.Tk()
    root = ctk.CTk()
    app = TiepNhanView(root)
    root.mainloop()