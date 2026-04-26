import tkinter as tk
from tkinter import ttk, messagebox

from app.db import get_connection, close_connection


class EmployeesWindow:
    """
    Окно раздела 'Сотрудники'.

    В этом окне отображается список сотрудников из базы данных.
    Дополнительно показывается название отдела, к которому относится сотрудник.
    """

    def __init__(self, parent):
        # Создаем дочернее окно.
        self.window = tk.Toplevel(parent)
        self.window.title("Сотрудники")
        self.window.geometry("1000x550")
        self.window.minsize(850, 450)

        # Таблица будет сохранена в этом атрибуте.
        self.tree = None

        self.create_widgets()
        self.load_employees()

    def create_widgets(self):
        """
        Создает элементы интерфейса окна:
        заголовок, кнопки, таблицу и полосу прокрутки.
        """
        title_label = tk.Label(
            self.window,
            text="Раздел: Сотрудники",
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
            command=self.load_employees
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

        # Создаем таблицу сотрудников.
        self.tree = ttk.Treeview(
            table_frame,
            columns=(
                "employee_id",
                "full_name",
                "work_experience",
                "gender",
                "department_name",
            ),
            show="headings"
        )

        # Настраиваем заголовки столбцов.
        self.tree.heading("employee_id", text="Табельный номер")
        self.tree.heading("full_name", text="ФИО")
        self.tree.heading("work_experience", text="Стаж")
        self.tree.heading("gender", text="Пол")
        self.tree.heading("department_name", text="Отдел")

        # Настраиваем ширину столбцов.
        self.tree.column("employee_id", width=140, anchor="center")
        self.tree.column("full_name", width=260, anchor="w")
        self.tree.column("work_experience", width=100, anchor="center")
        self.tree.column("gender", width=100, anchor="center")
        self.tree.column("department_name", width=250, anchor="w")

        # Добавляем вертикальную полосу прокрутки.
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Размещаем элементы.
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_employees(self):
        """
        Загружает сотрудников из базы данных и отображает их в таблице.
        """
        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return

        try:
            cursor = connection.cursor()

            # Получаем сотрудников вместе с названиями отделов.
            cursor.execute("""
                SELECT
                    e.employee_id,
                    CONCAT(e.last_name, ' ', e.first_name, ' ', e.middle_name) AS full_name,
                    e.work_experience,
                    e.gender,
                    d.department_name
                FROM employees e
                JOIN departments d ON e.department_id = d.department_id
                ORDER BY e.employee_id
            """)
            rows = cursor.fetchall()

            # Очищаем таблицу перед повторной загрузкой.
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Добавляем строки в таблицу.
            for row in rows:
                self.tree.insert("", "end", values=row)

            cursor.close()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось загрузить сотрудников:\n{error}")

        finally:
            close_connection(connection)