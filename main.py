import tkinter as tk

from app.gui.login_window import LoginWindow


def main():
    """
    Точка входа в приложение.

    Сначала открывается окно входа в систему.
    После успешной авторизации пользователь попадает в главное окно.
    """
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()