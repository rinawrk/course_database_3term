import tkinter as tk
from tkinter import ttk, messagebox

from app.db import get_connection, close_connection


class EmployeesWindow:
    """
    Окно раздела 'Сотрудники'.

    В этом окне отображается список сотрудников из базы данных.
    Также реализовано добавление нового сотрудника.
    """

    def __init__(self, parent):
        # Создаем дочернее окно.
        self.window = tk.Toplevel(parent)
        self.window.title("Сотрудники")
        self.window.geometry("1000x550")
        self.window.minsize(850, 450)

        # Таблица сотрудников.
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

        add_button = tk.Button(
            buttons_frame,
            text="Добавить сотрудника",
            font=("Arial", 11),
            width=20,
            command=self.open_add_employee_window
        )
        add_button.grid(row=0, column=0, padx=10)

        refresh_button = tk.Button(
            buttons_frame,
            text="Обновить список",
            font=("Arial", 11),
            width=18,
            command=self.load_employees
        )
        refresh_button.grid(row=0, column=1, padx=10)

        close_button = tk.Button(
            buttons_frame,
            text="Закрыть",
            font=("Arial", 11),
            width=18,
            command=self.window.destroy
        )
        close_button.grid(row=0, column=2, padx=10)

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

    def open_add_employee_window(self):
        """
        Открывает окно добавления сотрудника.
        """
        add_window = tk.Toplevel(self.window)
        add_window.title("Добавление сотрудника")

        # Увеличили высоту окна, чтобы кнопки точно помещались.
        add_window.geometry("420x620")

        # Разрешаем изменение размера окна пользователем.
        add_window.resizable(True, True)

        # Словарь: отображаемая строка -> department_id.
        department_map = {}

        tk.Label(add_window, text="Табельный номер:", font=("Arial", 11)).pack(pady=(15, 5))
        employee_id_entry = tk.Entry(add_window, font=("Arial", 11), width=30)
        employee_id_entry.pack()

        tk.Label(add_window, text="Фамилия:", font=("Arial", 11)).pack(pady=(10, 5))
        last_name_entry = tk.Entry(add_window, font=("Arial", 11), width=30)
        last_name_entry.pack()

        tk.Label(add_window, text="Имя:", font=("Arial", 11)).pack(pady=(10, 5))
        first_name_entry = tk.Entry(add_window, font=("Arial", 11), width=30)
        first_name_entry.pack()

        tk.Label(add_window, text="Отчество:", font=("Arial", 11)).pack(pady=(10, 5))
        middle_name_entry = tk.Entry(add_window, font=("Arial", 11), width=30)
        middle_name_entry.pack()

        tk.Label(add_window, text="Стаж работы:", font=("Arial", 11)).pack(pady=(10, 5))
        work_experience_entry = tk.Entry(add_window, font=("Arial", 11), width=30)
        work_experience_entry.pack()

        tk.Label(add_window, text="Пол:", font=("Arial", 11)).pack(pady=(10, 5))
        gender_combobox = ttk.Combobox(
            add_window,
            values=["М", "Ж"],
            state="readonly",
            width=27
        )
        gender_combobox.pack()

        tk.Label(add_window, text="Отдел:", font=("Arial", 11)).pack(pady=(10, 5))
        department_combobox = ttk.Combobox(
            add_window,
            state="readonly",
            width=27
        )
        department_combobox.pack()

        # Загружаем список отделов в выпадающий список.
        connection = get_connection()
        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT department_id, department_name
                    FROM departments
                    ORDER BY department_id
                """)
                departments = cursor.fetchall()

                values = []
                for department_id, department_name in departments:
                    display_value = f"{department_id} — {department_name}"
                    values.append(display_value)
                    department_map[display_value] = department_id

                department_combobox["values"] = values
                if values:
                    department_combobox.current(0)

                cursor.close()
            except Exception as error:
                messagebox.showerror("Ошибка", f"Не удалось загрузить отделы:\n{error}")
            finally:
                close_connection(connection)

        def save_employee():
            """
            Сохраняет нового сотрудника в базу данных.
            """
            employee_id = employee_id_entry.get().strip()
            last_name = last_name_entry.get().strip()
            first_name = first_name_entry.get().strip()
            middle_name = middle_name_entry.get().strip()
            work_experience = work_experience_entry.get().strip()
            gender = gender_combobox.get().strip()
            department_value = department_combobox.get().strip()

            if not all([
                employee_id,
                last_name,
                first_name,
                middle_name,
                work_experience,
                gender,
                department_value,
            ]):
                messagebox.showwarning("Предупреждение", "Заполните все поля.")
                return

            if not employee_id.isdigit():
                messagebox.showwarning("Предупреждение", "Табельный номер должен быть числом.")
                return

            if not work_experience.isdigit():
                messagebox.showwarning("Предупреждение", "Стаж работы должен быть числом.")
                return

            department_id = department_map.get(department_value)
            if department_id is None:
                messagebox.showwarning("Предупреждение", "Выберите корректный отдел.")
                return

            connection = get_connection()

            if connection is None:
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
                return

            try:
                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO employees (
                        employee_id,
                        last_name,
                        first_name,
                        middle_name,
                        work_experience,
                        gender,
                        department_id
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    int(employee_id),
                    last_name,
                    first_name,
                    middle_name,
                    int(work_experience),
                    gender,
                    department_id,
                ))

                connection.commit()
                cursor.close()

                messagebox.showinfo("Успех", "Сотрудник успешно добавлен.")
                add_window.destroy()
                self.load_employees()

            except Exception as error:
                messagebox.showerror("Ошибка", f"Не удалось добавить сотрудника:\n{error}")

            finally:
                close_connection(connection)

        tk.Button(
            add_window,
            text="Сохранить",
            font=("Arial", 11),
            width=16,
            command=save_employee
        ).pack(pady=(20, 5))

        tk.Button(
            add_window,
            text="Отмена",
            font=("Arial", 11),
            width=16,
            command=add_window.destroy
        ).pack(pady=5)