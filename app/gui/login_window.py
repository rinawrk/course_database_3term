import tkinter as tk
from tkinter import messagebox

from app.db import get_connection, close_connection


class LoginWindow:
    """
    Окно входа в систему.

    Пользователь вводит логин и пароль.
    Если данные верны, окно перестраивается в главное окно приложения.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Вход в систему")
        self.root.geometry("420x320")
        self.root.minsize(420, 320)

        self.login_entry = None
        self.password_entry = None

        self.create_widgets()

    def clear_window(self):
        """
        Удаляет все текущие элементы из главного окна.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):
        """
        Создает элементы интерфейса окна входа.
        """
        self.clear_window()

        self.root.title("Вход в систему")
        self.root.geometry("420x320")
        self.root.minsize(420, 320)

        title_label = tk.Label(
            self.root,
            text="Авторизация",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(35, 20))

        login_label = tk.Label(
            self.root,
            text="Логин:",
            font=("Arial", 11)
        )
        login_label.pack(pady=(5, 5))

        self.login_entry = tk.Entry(self.root, font=("Arial", 11), width=28)
        self.login_entry.pack(pady=(0, 10))
        self.login_entry.focus()

        password_label = tk.Label(
            self.root,
            text="Пароль:",
            font=("Arial", 11)
        )
        password_label.pack(pady=(5, 5))

        self.password_entry = tk.Entry(self.root, font=("Arial", 11), width=28, show="*")
        self.password_entry.pack(pady=(0, 20))

        login_button = tk.Button(
            self.root,
            text="Войти",
            font=("Arial", 11),
            width=18,
            command=self.authenticate_user
        )
        login_button.pack(pady=(5, 8))

        exit_button = tk.Button(
            self.root,
            text="Выход",
            font=("Arial", 11),
            width=18,
            command=self.root.destroy
        )
        exit_button.pack()

        # Позволяем входить по нажатию Enter.
        self.root.bind("<Return>", lambda event: self.authenticate_user())

    def authenticate_user(self):
        """
        Проверяет логин и пароль в таблице users.

        Если пользователь найден, очищает текущее окно
        и открывает главное окно приложения.
        """
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()

        if not login or not password:
            messagebox.showwarning("Предупреждение", "Введите логин и пароль.")
            return

        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT login, role
                FROM users
                WHERE login = %s AND password = %s
            """, (login, password))
            user = cursor.fetchone()
            cursor.close()

            if user is None:
                messagebox.showerror("Ошибка", "Неверный логин или пароль.")
                return

            user_login = user[0]
            user_role = user[1]

            self.clear_window()

            # Локальный импорт нужен, чтобы избежать циклического импорта.
            from app.gui.main_window import MainWindow
            MainWindow(self.root, user_login, user_role)

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось выполнить вход:\n{error}")

        finally:
            close_connection(connection)