import tkinter as tk
from tkinter import messagebox

from app.db import get_connection, close_connection
from app.gui.departments_window import DepartmentsWindow
from app.gui.employees_window import EmployeesWindow
from app.gui.children_window import ChildrenWindow
from app.gui.reports_window import ReportsWindow


class MainWindow:
    """
    Главное окно приложения.
    Содержит кнопки перехода в основные разделы и кнопку проверки подключения к БД.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Отдел кадров")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)

        self.create_widgets()

    def create_widgets(self):
        """
        Создает элементы интерфейса главного окна.
        """
        title_label = tk.Label(
            self.root,
            text="Курсовой проект: Отдел кадров",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=(30, 10))

        info_label = tk.Label(
            self.root,
            text="Десктоп-приложение для работы с базой данных сотрудников и детей.",
            font=("Arial", 12)
        )
        info_label.pack(pady=(0, 25))

        # Рамка для основных кнопок навигации.
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10)

        departments_button = tk.Button(
            buttons_frame,
            text="Отделы",
            font=("Arial", 12),
            width=20,
            command=self.open_departments_window
        )
        departments_button.grid(row=0, column=0, padx=10, pady=10)

        employees_button = tk.Button(
            buttons_frame,
            text="Сотрудники",
            font=("Arial", 12),
            width=20,
            command=self.open_employees_window
        )
        employees_button.grid(row=0, column=1, padx=10, pady=10)

        children_button = tk.Button(
            buttons_frame,
            text="Дети",
            font=("Arial", 12),
            width=20,
            command=self.open_children_window
        )
        children_button.grid(row=1, column=0, padx=10, pady=10)

        reports_button = tk.Button(
            buttons_frame,
            text="Отчеты",
            font=("Arial", 12),
            width=20,
            command=self.open_reports_window
        )
        reports_button.grid(row=1, column=1, padx=10, pady=10)

        check_button = tk.Button(
            self.root,
            text="Проверить подключение к БД",
            font=("Arial", 12),
            width=28,
            command=self.check_database_connection
        )
        check_button.pack(pady=(25, 10))

        exit_button = tk.Button(
            self.root,
            text="Выход",
            font=("Arial", 12),
            width=18,
            command=self.root.destroy
        )
        exit_button.pack(pady=10)

    def open_departments_window(self):
        """
        Открывает окно раздела 'Отделы'.
        """
        DepartmentsWindow(self.root)

    def open_employees_window(self):
        """
        Открывает окно раздела 'Сотрудники'.
        """
        EmployeesWindow(self.root)

    def open_children_window(self):
        """
        Открывает окно раздела 'Дети'.
        """
        ChildrenWindow(self.root)

    def open_reports_window(self):
        """
        Открывает окно раздела 'Отчеты'.
        """
        ReportsWindow(self.root)

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