import tkinter as tk
from tkinter import ttk, messagebox

from app.db import get_connection, close_connection


class ReportsWindow:
    """
    Окно раздела 'Отчеты'.

    В этом окне можно:
    1. Выбрать отдел и получить отчет по детям сотрудников этого отдела.
    2. Получить общий сгруппированный список по всей базе данных.
    """

    def __init__(self, parent):
        # Создаем дочернее окно.
        self.window = tk.Toplevel(parent)
        self.window.title("Отчеты")
        self.window.geometry("1100x600")
        self.window.minsize(900, 500)

        # Таблица для вывода результата отчета.
        self.tree = None

        # Словарь для соответствия отображаемой строки и ID отдела.
        self.department_map = {}

        # Combobox для выбора отдела.
        self.department_combobox = None

        # Текстовая строка с названием текущего отчета.
        self.report_title_label = None

        self.create_widgets()
        self.load_departments()

    def create_widgets(self):
        """
        Создает элементы интерфейса окна отчетов.
        """
        title_label = tk.Label(
            self.window,
            text="Раздел: Отчеты",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(20, 10))

        info_label = tk.Label(
            self.window,
            text="Выберите отдел для первого отчета или откройте общий отчет по всей базе данных.",
            font=("Arial", 11)
        )
        info_label.pack(pady=(0, 15))

        # Верхняя панель с элементами управления.
        controls_frame = tk.Frame(self.window)
        controls_frame.pack(pady=(0, 15))

        department_label = tk.Label(
            controls_frame,
            text="Отдел:",
            font=("Arial", 11)
        )
        department_label.grid(row=0, column=0, padx=(0, 8), pady=5)

        self.department_combobox = ttk.Combobox(
            controls_frame,
            state="readonly",
            width=35
        )
        self.department_combobox.grid(row=0, column=1, padx=8, pady=5)

        report_one_button = tk.Button(
            controls_frame,
            text="Дети сотрудников отдела",
            font=("Arial", 11),
            width=24,
            command=self.show_children_by_department_report
        )
        report_one_button.grid(row=0, column=2, padx=8, pady=5)

        report_two_button = tk.Button(
            controls_frame,
            text="Общий сгруппированный отчет",
            font=("Arial", 11),
            width=28,
            command=self.show_full_grouped_report
        )
        report_two_button.grid(row=0, column=3, padx=8, pady=5)

        close_button = tk.Button(
            controls_frame,
            text="Закрыть",
            font=("Arial", 11),
            width=14,
            command=self.window.destroy
        )
        close_button.grid(row=0, column=4, padx=8, pady=5)

        # Подпись, показывающая, какой отчет сейчас открыт.
        self.report_title_label = tk.Label(
            self.window,
            text="Отчет пока не выбран",
            font=("Arial", 12, "bold")
        )
        self.report_title_label.pack(pady=(0, 10))

        # Рамка для таблицы.
        table_frame = tk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Начально создаем пустую таблицу.
        self.tree = ttk.Treeview(table_frame, show="headings")

        # Вертикальная прокрутка.
        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=vertical_scrollbar.set)

        # Горизонтальная прокрутка.
        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )
        self.tree.configure(xscrollcommand=horizontal_scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

    def load_departments(self):
        """
        Загружает список отделов в выпадающий список.
        """
        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT department_id, department_name
                FROM departments
                ORDER BY department_id
            """)
            rows = cursor.fetchall()

            self.department_map.clear()
            values = []

            for department_id, department_name in rows:
                display_value = f"{department_id} — {department_name}"
                values.append(display_value)
                self.department_map[display_value] = department_id

            self.department_combobox["values"] = values

            if values:
                self.department_combobox.current(0)

            cursor.close()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось загрузить список отделов:\n{error}")

        finally:
            close_connection(connection)

    def configure_tree(self, columns, headings, widths):
        """
        Полностью перенастраивает таблицу под нужный отчет.

        :param columns: внутренние имена колонок
        :param headings: заголовки колонок для пользователя
        :param widths: ширина колонок
        """
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = columns

        for column in columns:
            self.tree.heading(column, text="")

        for index, column in enumerate(columns):
            self.tree.heading(column, text=headings[index])
            self.tree.column(column, width=widths[index], anchor="w")

    def clear_tree(self):
        """
        Очищает строки текущей таблицы.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

    def show_children_by_department_report(self):
        """
        Формирует отчет:
        'Информация о детях сотрудников определенного отдела'.
        """
        selected_value = self.department_combobox.get()

        if not selected_value:
            messagebox.showwarning("Предупреждение", "Сначала выберите отдел.")
            return

        department_id = self.department_map.get(selected_value)

        if department_id is None:
            messagebox.showwarning("Предупреждение", "Не удалось определить выбранный отдел.")
            return

        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    d.department_name,
                    e.employee_id,
                    CONCAT(e.last_name, ' ', e.first_name, ' ', e.middle_name) AS employee_full_name,
                    c.birth_certificate_number,
                    c.child_name,
                    c.birth_year,
                    c.gender
                FROM departments d
                JOIN employees e ON e.department_id = d.department_id
                JOIN children c ON c.employee_id = e.employee_id
                WHERE d.department_id = %s
                ORDER BY e.last_name, e.first_name, c.child_name
            """, (department_id,))
            rows = cursor.fetchall()

            columns = (
                "department_name",
                "employee_id",
                "employee_full_name",
                "birth_certificate_number",
                "child_name",
                "birth_year",
                "gender",
            )
            headings = (
                "Отдел",
                "Табельный номер",
                "Сотрудник",
                "№ свидетельства",
                "Имя ребенка",
                "Год рождения",
                "Пол ребенка",
            )
            widths = (180, 130, 240, 140, 150, 120, 100)

            self.configure_tree(columns, headings, widths)
            self.clear_tree()

            for row in rows:
                self.tree.insert("", "end", values=row)

            self.report_title_label.config(
                text="Отчет: Дети сотрудников выбранного отдела"
            )

            if not rows:
                messagebox.showinfo("Информация", "Для выбранного отдела записи не найдены.")

            cursor.close()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось сформировать отчет:\n{error}")

        finally:
            close_connection(connection)

    def show_full_grouped_report(self):
        """
        Формирует отчет:
        'Сгруппированный список всей базы данных'.
        """
        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    d.department_name,
                    CONCAT(e.last_name, ' ', e.first_name, ' ', e.middle_name) AS employee_full_name,
                    e.work_experience,
                    e.gender,
                    c.child_name,
                    c.birth_year,
                    c.gender
                FROM departments d
                LEFT JOIN employees e ON e.department_id = d.department_id
                LEFT JOIN children c ON c.employee_id = e.employee_id
                ORDER BY d.department_name, e.last_name, e.first_name, c.child_name
            """)
            rows = cursor.fetchall()

            columns = (
                "department_name",
                "employee_full_name",
                "work_experience",
                "employee_gender",
                "child_name",
                "birth_year",
                "child_gender",
            )
            headings = (
                "Отдел",
                "Сотрудник",
                "Стаж",
                "Пол сотрудника",
                "Имя ребенка",
                "Год рождения ребенка",
                "Пол ребенка",
            )
            widths = (180, 240, 100, 120, 150, 150, 120)

            self.configure_tree(columns, headings, widths)
            self.clear_tree()

            for row in rows:
                self.tree.insert("", "end", values=row)

            self.report_title_label.config(
                text="Отчет: Сгруппированный список всей базы данных"
            )

            if not rows:
                messagebox.showinfo("Информация", "Данные для отчета не найдены.")

            cursor.close()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось сформировать общий отчет:\n{error}")

        finally:
            close_connection(connection)