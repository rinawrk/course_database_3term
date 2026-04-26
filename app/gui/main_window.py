import tkinter as tk
from tkinter import messagebox

from app.db import get_connection, close_connection


class MainWindow:
    """
    Главное окно приложения.
    Пока оно содержит только заголовок, описание и кнопку проверки подключения к БД.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Отдел кадров")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)

        self.create_widgets()

    def create_widgets(self):
        """
        Создает виджеты главного окна.
        """
        title_label = tk.Label(
            self.root,
            text="Курсовой проект: Отдел кадров",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(30, 10))

        info_label = tk.Label(
            self.root,
            text="Десктоп-приложение для работы с базой данных сотрудников и детей.",
            font=("Arial", 12)
        )
        info_label.pack(pady=(0, 20))

        check_button = tk.Button(
            self.root,
            text="Проверить подключение к БД",
            font=("Arial", 12),
            width=25,
            command=self.check_database_connection
        )
        check_button.pack(pady=10)

    def check_database_connection(self):
        """
        Проверяет подключение к базе данных и показывает результат пользователю.
        """
        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            result = cursor.fetchone()

            database_name = result[0] if result else "не определена"
            messagebox.showinfo(
                "Успех",
                f"Подключение выполнено успешно.\nТекущая база данных: {database_name}"
            )
            cursor.close()
        finally:
            close_connection(connection)