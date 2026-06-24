import customtkinter as ctk

from app_context import AppContext
from views.login_view import LoginView


APP_WIDTH = 1520
APP_HEIGHT = 820


def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Hệ thống mô phỏng hàng đợi dịch vụ")
    root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
    root.minsize(APP_WIDTH, APP_HEIGHT)
    root.maxsize(APP_WIDTH, APP_HEIGHT)
    root.resizable(False, False)

    app_context = AppContext(root)
    LoginView(root, app_context).show()

    root.mainloop()


if __name__ == "__main__":
    main()
