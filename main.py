import tkinter as tk

from app_context import AppContext
from views.login_view import LoginView


def main():
    root = tk.Tk()
    root.title("Hệ thống mô phỏng hàng đợi ngân hàng")
    root.geometry("900x600")
    root.resizable(False, False)

    app_context = AppContext(root)

    LoginView(root, app_context).show()

    root.mainloop()


if __name__ == "__main__":
    main()