import tkinter as tk
from tkinter import ttk, messagebox

from app.db import get_connection, close_connection


class DepartmentsWindow:
    """
    Окно раздела 'Отделы'.

    В этом окне отображается список отделов из базы данных.
    Пока здесь реализован только просмотр данных и обновление таблицы.
    """

    def __init__(self, parent):
        # Создаем отдельное дочернее окно.
        self.window = tk.Toplevel(parent)
        self.window.title("Отделы")
        self.window.geometry("800x500")
        self.window.minsize(700, 400)

        # Здесь будет храниться таблица с данными.
        self.tree = None

        self.create_widgets()
        self.load_departments()

    def create_widgets(self):
        """
        Создает элементы интерфейса окна:
        заголовок, кнопки и таблицу отделов.
        """
        title_label = tk.Label(
            self.window,
            text="Раздел: Отделы",
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
            command=self.load_departments
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

        # Рамка для таблицы и полосы прокрутки.
        table_frame = tk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Создаем таблицу.
        self.tree = ttk.Treeview(
            table_frame,
            columns=("department_id", "department_name"),
            show="headings"
        )

        # Настраиваем заголовки столбцов.
        self.tree.heading("department_id", text="Номер отдела")
        self.tree.heading("department_name", text="Название отдела")

        # Настраиваем ширину столбцов.
        self.tree.column("department_id", width=150, anchor="center")
        self.tree.column("department_name", width=500, anchor="w")

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

    def load_departments(self):
        """
        Загружает список отделов из базы данных и отображает его в таблице.
        """
        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return

        try:
            cursor = connection.cursor()

            # Получаем список отделов из базы данных.
            cursor.execute("""
                SELECT department_id, department_name
                FROM departments
                ORDER BY department_id
            """)
            rows = cursor.fetchall()

            # Очищаем текущие строки таблицы перед новой загрузкой.
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Добавляем строки в таблицу.
            for row in rows:
                self.tree.insert("", "end", values=row)

            cursor.close()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось загрузить отделы:\n{error}")

        finally:
            close_connection(connection)