import tkinter as tk
from tkinter import ttk, messagebox

from app.db import get_connection, close_connection


class EmployeesWindow:
    """
    Окно раздела 'Сотрудники'.

    В этом окне отображается список сотрудников из базы данных.
    Реализованы:
    - просмотр списка;
    - добавление нового сотрудника;
    - редактирование выбранного сотрудника;
    - удаление сотрудника.
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
        add_button.grid(row=0, column=0, padx=8)

        edit_button = tk.Button(
            buttons_frame,
            text="Изменить сотрудника",
            font=("Arial", 11),
            width=20,
            command=self.open_edit_employee_window
        )
        edit_button.grid(row=0, column=1, padx=8)

        delete_button = tk.Button(
            buttons_frame,
            text="Удалить сотрудника",
            font=("Arial", 11),
            width=20,
            command=self.delete_employee
        )
        delete_button.grid(row=0, column=2, padx=8)

        refresh_button = tk.Button(
            buttons_frame,
            text="Обновить список",
            font=("Arial", 11),
            width=18,
            command=self.load_employees
        )
        refresh_button.grid(row=0, column=3, padx=8)

        close_button = tk.Button(
            buttons_frame,
            text="Закрыть",
            font=("Arial", 11),
            width=18,
            command=self.window.destroy
        )
        close_button.grid(row=0, column=4, padx=8)

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

    def get_departments_for_combobox(self):
        """
        Загружает список отделов для выпадающего списка.

        Возвращает:
        - список строк для Combobox;
        - словарь вида {отображаемая строка: department_id}.
        """
        department_map = {}
        values = []

        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return values, department_map

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT department_id, department_name
                FROM departments
                ORDER BY department_id
            """)
            departments = cursor.fetchall()

            for department_id, department_name in departments:
                display_value = f"{department_id} — {department_name}"
                values.append(display_value)
                department_map[display_value] = department_id

            cursor.close()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось загрузить отделы:\n{error}")

        finally:
            close_connection(connection)

        return values, department_map

    def open_add_employee_window(self):
        """
        Открывает окно добавления сотрудника.
        """
        add_window = tk.Toplevel(self.window)
        add_window.title("Добавление сотрудника")
        add_window.geometry("420x620")
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

        # Загружаем отделы в выпадающий список.
        values, department_map = self.get_departments_for_combobox()
        department_combobox["values"] = values
        if values:
            department_combobox.current(0)

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

    def open_edit_employee_window(self):
        """
        Открывает окно редактирования выбранного сотрудника.
        """
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Сначала выберите сотрудника в таблице.")
            return

        values = self.tree.item(selected_item[0], "values")
        employee_id = values[0]

        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    employee_id,
                    last_name,
                    first_name,
                    middle_name,
                    work_experience,
                    gender,
                    department_id
                FROM employees
                WHERE employee_id = %s
            """, (employee_id,))
            employee = cursor.fetchone()
            cursor.close()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные сотрудника:\n{error}")
            return

        finally:
            close_connection(connection)

        if employee is None:
            messagebox.showwarning("Предупреждение", "Сотрудник не найден.")
            return

        edit_window = tk.Toplevel(self.window)
        edit_window.title("Редактирование сотрудника")
        edit_window.geometry("420x620")
        edit_window.resizable(True, True)

        current_employee_id = employee[0]
        current_last_name = employee[1]
        current_first_name = employee[2]
        current_middle_name = employee[3]
        current_work_experience = employee[4]
        current_gender = employee[5]
        current_department_id = employee[6]

        tk.Label(edit_window, text="Табельный номер:", font=("Arial", 11)).pack(pady=(15, 5))
        employee_id_entry = tk.Entry(edit_window, font=("Arial", 11), width=30)
        employee_id_entry.pack()
        employee_id_entry.insert(0, str(current_employee_id))
        employee_id_entry.config(state="disabled")

        tk.Label(edit_window, text="Фамилия:", font=("Arial", 11)).pack(pady=(10, 5))
        last_name_entry = tk.Entry(edit_window, font=("Arial", 11), width=30)
        last_name_entry.pack()
        last_name_entry.insert(0, current_last_name)

        tk.Label(edit_window, text="Имя:", font=("Arial", 11)).pack(pady=(10, 5))
        first_name_entry = tk.Entry(edit_window, font=("Arial", 11), width=30)
        first_name_entry.pack()
        first_name_entry.insert(0, current_first_name)

        tk.Label(edit_window, text="Отчество:", font=("Arial", 11)).pack(pady=(10, 5))
        middle_name_entry = tk.Entry(edit_window, font=("Arial", 11), width=30)
        middle_name_entry.pack()
        middle_name_entry.insert(0, current_middle_name)

        tk.Label(edit_window, text="Стаж работы:", font=("Arial", 11)).pack(pady=(10, 5))
        work_experience_entry = tk.Entry(edit_window, font=("Arial", 11), width=30)
        work_experience_entry.pack()
        work_experience_entry.insert(0, str(current_work_experience))

        tk.Label(edit_window, text="Пол:", font=("Arial", 11)).pack(pady=(10, 5))
        gender_combobox = ttk.Combobox(
            edit_window,
            values=["М", "Ж"],
            state="readonly",
            width=27
        )
        gender_combobox.pack()
        gender_combobox.set(current_gender)

        tk.Label(edit_window, text="Отдел:", font=("Arial", 11)).pack(pady=(10, 5))
        department_combobox = ttk.Combobox(
            edit_window,
            state="readonly",
            width=27
        )
        department_combobox.pack()

        # Загружаем отделы и выбираем текущий отдел сотрудника.
        department_values, department_map = self.get_departments_for_combobox()
        department_combobox["values"] = department_values

        for display_value, department_id in department_map.items():
            if department_id == current_department_id:
                department_combobox.set(display_value)
                break

        def update_employee():
            """
            Сохраняет изменения выбранного сотрудника в базе данных.
            """
            last_name = last_name_entry.get().strip()
            first_name = first_name_entry.get().strip()
            middle_name = middle_name_entry.get().strip()
            work_experience = work_experience_entry.get().strip()
            gender = gender_combobox.get().strip()
            department_value = department_combobox.get().strip()

            if not all([
                last_name,
                first_name,
                middle_name,
                work_experience,
                gender,
                department_value,
            ]):
                messagebox.showwarning("Предупреждение", "Заполните все поля.")
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
                    UPDATE employees
                    SET
                        last_name = %s,
                        first_name = %s,
                        middle_name = %s,
                        work_experience = %s,
                        gender = %s,
                        department_id = %s
                    WHERE employee_id = %s
                """, (
                    last_name,
                    first_name,
                    middle_name,
                    int(work_experience),
                    gender,
                    department_id,
                    int(current_employee_id),
                ))

                connection.commit()
                cursor.close()

                messagebox.showinfo("Успех", "Сотрудник успешно изменен.")
                edit_window.destroy()
                self.load_employees()

            except Exception as error:
                messagebox.showerror("Ошибка", f"Не удалось изменить сотрудника:\n{error}")

            finally:
                close_connection(connection)

        tk.Button(
            edit_window,
            text="Сохранить",
            font=("Arial", 11),
            width=16,
            command=update_employee
        ).pack(pady=(20, 5))

        tk.Button(
            edit_window,
            text="Отмена",
            font=("Arial", 11),
            width=16,
            command=edit_window.destroy
        ).pack(pady=5)

    def delete_employee(self):
        """
        Удаляет выбранного сотрудника из базы данных.

        Перед удалением проверяется:
        1. выбран ли сотрудник;
        2. нет ли у него связанных записей в таблице children.
        """
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Сначала выберите сотрудника в таблице.")
            return

        values = self.tree.item(selected_item[0], "values")
        employee_id = int(values[0])
        employee_name = values[1]

        confirm = messagebox.askyesno(
            "Подтверждение",
            f"Удалить сотрудника '{employee_name}'?"
        )

        if not confirm:
            return

        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return

        try:
            cursor = connection.cursor()

            # Проверяем, есть ли у сотрудника дети.
            cursor.execute("""
                SELECT COUNT(*)
                FROM children
                WHERE employee_id = %s
            """, (employee_id,))
            children_count = cursor.fetchone()[0]

            if children_count > 0:
                messagebox.showwarning(
                    "Предупреждение",
                    "Нельзя удалить сотрудника, у которого есть дети в базе данных."
                )
                cursor.close()
                return

            # Если связанных детей нет, удаляем сотрудника.
            cursor.execute("""
                DELETE FROM employees
                WHERE employee_id = %s
            """, (employee_id,))
            connection.commit()
            cursor.close()

            messagebox.showinfo("Успех", "Сотрудник успешно удален.")
            self.load_employees()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось удалить сотрудника:\n{error}")

        finally:
            close_connection(connection)