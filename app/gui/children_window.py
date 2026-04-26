import tkinter as tk
from tkinter import ttk, messagebox

from app.db import get_connection, close_connection


class ChildrenWindow:
    """
    Окно раздела 'Дети'.

    В этом окне отображается список детей из базы данных.
    Дополнительно показывается ФИО сотрудника, к которому относится ребенок.
    """

    def __init__(self, parent):
        # Создаем дочернее окно.
        self.window = tk.Toplevel(parent)
        self.window.title("Дети")
        self.window.geometry("1000x550")
        self.window.minsize(850, 450)

        # Таблица будет храниться в этом атрибуте.
        self.tree = None

        self.create_widgets()
        self.load_children()

    def create_widgets(self):
        """
        Создает элементы интерфейса окна:
        заголовок, кнопки, таблицу и полосу прокрутки.
        """
        title_label = tk.Label(
            self.window,
            text="Раздел: Дети",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(20, 10))

        # Верхняя панель с кнопками.
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=(0, 15))

        refresh_button = tk.Button(
            buttons_frame,
            text="Обновить список",
            font=("Arial", 11),
            width=18,
            command=self.load_children
        )
        refresh_button.grid(row=0, column=0, padx=10)

        close_button = tk.Button(
            buttons_frame,
            text="Закрыть",
            font=("Arial", 11),
            width=18,
            command=self.window.destroy
        )
        close_button.grid(row=0, column=1, padx=10)

        # Рамка для таблицы.
        table_frame = tk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Создаем таблицу детей.
        self.tree = ttk.Treeview(
            table_frame,
            columns=(
                "birth_certificate_number",
                "child_name",
                "birth_year",
                "gender",
                "employee_full_name",
            ),
            show="headings"
        )

        # Заголовки столбцов.
        self.tree.heading("birth_certificate_number", text="№ свидетельства")
        self.tree.heading("child_name", text="Имя ребенка")
        self.tree.heading("birth_year", text="Год рождения")
        self.tree.heading("gender", text="Пол")
        self.tree.heading("employee_full_name", text="Сотрудник")

        # Ширина столбцов.
        self.tree.column("birth_certificate_number", width=160, anchor="center")
        self.tree.column("child_name", width=180, anchor="w")
        self.tree.column("birth_year", width=120, anchor="center")
        self.tree.column("gender", width=100, anchor="center")
        self.tree.column("employee_full_name", width=320, anchor="w")

        # Вертикальная полоса прокрутки.
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Размещаем таблицу и скролл.
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_children(self):
        """
        Загружает список детей из базы данных и отображает его в таблице.
        """
        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return

        try:
            cursor = connection.cursor()

            # Получаем список детей вместе с ФИО сотрудников.
            cursor.execute("""
                SELECT
                    c.birth_certificate_number,
                    c.child_name,
                    c.birth_year,
                    c.gender,
                    CONCAT(e.last_name, ' ', e.first_name, ' ', e.middle_name) AS employee_full_name
                FROM children c
                JOIN employees e ON c.employee_id = e.employee_id
                ORDER BY c.birth_certificate_number
            """)
            rows = cursor.fetchall()

            # Очищаем таблицу перед новой загрузкой.
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Добавляем строки в таблицу.
            for row in rows:
                self.tree.insert("", "end", values=row)

            cursor.close()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось загрузить список детей:\n{error}")

        finally:
            close_connection(connection)