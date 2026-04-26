import tkinter as tk
from tkinter import ttk, messagebox

from app.db import get_connection, close_connection


class ChildrenWindow:
    """
    Окно раздела 'Дети'.

    В этом окне отображается список детей из базы данных.
    Дополнительно показывается ФИО сотрудника, к которому относится ребенок.

    Реализованы:
    - просмотр списка;
    - добавление нового ребенка;
    - редактирование выбранного ребенка.
    """

    def __init__(self, parent):
        # Создаем дочернее окно.
        self.window = tk.Toplevel(parent)
        self.window.title("Дети")
        self.window.geometry("1000x550")
        self.window.minsize(850, 450)

        # Таблица детей.
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

        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=(0, 15))

        add_button = tk.Button(
            buttons_frame,
            text="Добавить ребенка",
            font=("Arial", 11),
            width=18,
            command=self.open_add_child_window
        )
        add_button.grid(row=0, column=0, padx=8)

        edit_button = tk.Button(
            buttons_frame,
            text="Изменить ребенка",
            font=("Arial", 11),
            width=18,
            command=self.open_edit_child_window
        )
        edit_button.grid(row=0, column=1, padx=8)

        refresh_button = tk.Button(
            buttons_frame,
            text="Обновить список",
            font=("Arial", 11),
            width=18,
            command=self.load_children
        )
        refresh_button.grid(row=0, column=2, padx=8)

        close_button = tk.Button(
            buttons_frame,
            text="Закрыть",
            font=("Arial", 11),
            width=18,
            command=self.window.destroy
        )
        close_button.grid(row=0, column=3, padx=8)

        table_frame = tk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

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

        self.tree.heading("birth_certificate_number", text="№ свидетельства")
        self.tree.heading("child_name", text="Имя ребенка")
        self.tree.heading("birth_year", text="Год рождения")
        self.tree.heading("gender", text="Пол")
        self.tree.heading("employee_full_name", text="Сотрудник")

        self.tree.column("birth_certificate_number", width=160, anchor="center")
        self.tree.column("child_name", width=180, anchor="w")
        self.tree.column("birth_year", width=120, anchor="center")
        self.tree.column("gender", width=100, anchor="center")
        self.tree.column("employee_full_name", width=320, anchor="w")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

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

            for item in self.tree.get_children():
                self.tree.delete(item)

            for row in rows:
                self.tree.insert("", "end", values=row)

            cursor.close()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось загрузить список детей:\n{error}")

        finally:
            close_connection(connection)

    def get_employees_for_combobox(self):
        """
        Загружает список сотрудников для выпадающего списка.

        Возвращает:
        - список строк для Combobox;
        - словарь вида {отображаемая строка: employee_id}.
        """
        employee_map = {}
        values = []

        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return values, employee_map

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    employee_id,
                    CONCAT(last_name, ' ', first_name, ' ', middle_name) AS full_name
                FROM employees
                ORDER BY employee_id
            """)
            employees = cursor.fetchall()

            for employee_id, full_name in employees:
                display_value = f"{employee_id} — {full_name}"
                values.append(display_value)
                employee_map[display_value] = employee_id

            cursor.close()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось загрузить сотрудников:\n{error}")

        finally:
            close_connection(connection)

        return values, employee_map

    def open_add_child_window(self):
        """
        Открывает окно добавления ребенка.
        """
        add_window = tk.Toplevel(self.window)
        add_window.title("Добавление ребенка")
        add_window.geometry("420x500")
        add_window.resizable(True, True)

        employee_map = {}

        tk.Label(add_window, text="№ свидетельства о рождении:", font=("Arial", 11)).pack(pady=(15, 5))
        birth_certificate_entry = tk.Entry(add_window, font=("Arial", 11), width=30)
        birth_certificate_entry.pack()

        tk.Label(add_window, text="Имя ребенка:", font=("Arial", 11)).pack(pady=(10, 5))
        child_name_entry = tk.Entry(add_window, font=("Arial", 11), width=30)
        child_name_entry.pack()

        tk.Label(add_window, text="Год рождения:", font=("Arial", 11)).pack(pady=(10, 5))
        birth_year_entry = tk.Entry(add_window, font=("Arial", 11), width=30)
        birth_year_entry.pack()

        tk.Label(add_window, text="Пол:", font=("Arial", 11)).pack(pady=(10, 5))
        gender_combobox = ttk.Combobox(
            add_window,
            values=["М", "Ж"],
            state="readonly",
            width=27
        )
        gender_combobox.pack()

        tk.Label(add_window, text="Сотрудник:", font=("Arial", 11)).pack(pady=(10, 5))
        employee_combobox = ttk.Combobox(
            add_window,
            state="readonly",
            width=27
        )
        employee_combobox.pack()

        values, employee_map = self.get_employees_for_combobox()
        employee_combobox["values"] = values
        if values:
            employee_combobox.current(0)

        def save_child():
            """
            Сохраняет нового ребенка в базу данных.
            """
            birth_certificate_number = birth_certificate_entry.get().strip()
            child_name = child_name_entry.get().strip()
            birth_year = birth_year_entry.get().strip()
            gender = gender_combobox.get().strip()
            employee_value = employee_combobox.get().strip()

            if not all([
                birth_certificate_number,
                child_name,
                birth_year,
                gender,
                employee_value,
            ]):
                messagebox.showwarning("Предупреждение", "Заполните все поля.")
                return

            if not birth_certificate_number.isdigit():
                messagebox.showwarning("Предупреждение", "Номер свидетельства должен быть числом.")
                return

            if not birth_year.isdigit():
                messagebox.showwarning("Предупреждение", "Год рождения должен быть числом.")
                return

            birth_year_int = int(birth_year)
            if birth_year_int < 2000 or birth_year_int > 2100:
                messagebox.showwarning("Предупреждение", "Введите корректный год рождения.")
                return

            employee_id = employee_map.get(employee_value)
            if employee_id is None:
                messagebox.showwarning("Предупреждение", "Выберите корректного сотрудника.")
                return

            connection = get_connection()

            if connection is None:
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
                return

            try:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO children (
                        birth_certificate_number,
                        child_name,
                        birth_year,
                        gender,
                        employee_id
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    int(birth_certificate_number),
                    child_name,
                    birth_year_int,
                    gender,
                    employee_id,
                ))

                connection.commit()
                cursor.close()

                messagebox.showinfo("Успех", "Ребенок успешно добавлен.")
                add_window.destroy()
                self.load_children()

            except Exception as error:
                messagebox.showerror("Ошибка", f"Не удалось добавить ребенка:\n{error}")

            finally:
                close_connection(connection)

        tk.Button(
            add_window,
            text="Сохранить",
            font=("Arial", 11),
            width=16,
            command=save_child
        ).pack(pady=(20, 5))

        tk.Button(
            add_window,
            text="Отмена",
            font=("Arial", 11),
            width=16,
            command=add_window.destroy
        ).pack(pady=5)

    def open_edit_child_window(self):
        """
        Открывает окно редактирования выбранного ребенка.
        """
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Сначала выберите ребенка в таблице.")
            return

        values = self.tree.item(selected_item[0], "values")
        birth_certificate_number = values[0]

        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    birth_certificate_number,
                    child_name,
                    birth_year,
                    gender,
                    employee_id
                FROM children
                WHERE birth_certificate_number = %s
            """, (birth_certificate_number,))
            child = cursor.fetchone()
            cursor.close()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные ребенка:\n{error}")
            return

        finally:
            close_connection(connection)

        if child is None:
            messagebox.showwarning("Предупреждение", "Ребенок не найден.")
            return

        edit_window = tk.Toplevel(self.window)
        edit_window.title("Редактирование ребенка")
        edit_window.geometry("420x500")
        edit_window.resizable(True, True)

        current_birth_certificate_number = child[0]
        current_child_name = child[1]
        current_birth_year = child[2]
        current_gender = child[3]
        current_employee_id = child[4]

        tk.Label(edit_window, text="№ свидетельства о рождении:", font=("Arial", 11)).pack(pady=(15, 5))
        birth_certificate_entry = tk.Entry(edit_window, font=("Arial", 11), width=30)
        birth_certificate_entry.pack()
        birth_certificate_entry.insert(0, str(current_birth_certificate_number))
        birth_certificate_entry.config(state="disabled")

        tk.Label(edit_window, text="Имя ребенка:", font=("Arial", 11)).pack(pady=(10, 5))
        child_name_entry = tk.Entry(edit_window, font=("Arial", 11), width=30)
        child_name_entry.pack()
        child_name_entry.insert(0, current_child_name)

        tk.Label(edit_window, text="Год рождения:", font=("Arial", 11)).pack(pady=(10, 5))
        birth_year_entry = tk.Entry(edit_window, font=("Arial", 11), width=30)
        birth_year_entry.pack()
        birth_year_entry.insert(0, str(current_birth_year))

        tk.Label(edit_window, text="Пол:", font=("Arial", 11)).pack(pady=(10, 5))
        gender_combobox = ttk.Combobox(
            edit_window,
            values=["М", "Ж"],
            state="readonly",
            width=27
        )
        gender_combobox.pack()
        gender_combobox.set(current_gender)

        tk.Label(edit_window, text="Сотрудник:", font=("Arial", 11)).pack(pady=(10, 5))
        employee_combobox = ttk.Combobox(
            edit_window,
            state="readonly",
            width=27
        )
        employee_combobox.pack()

        employee_values, employee_map = self.get_employees_for_combobox()
        employee_combobox["values"] = employee_values

        for display_value, employee_id in employee_map.items():
            if employee_id == current_employee_id:
                employee_combobox.set(display_value)
                break

        def update_child():
            """
            Сохраняет изменения выбранного ребенка в базе данных.
            """
            child_name = child_name_entry.get().strip()
            birth_year = birth_year_entry.get().strip()
            gender = gender_combobox.get().strip()
            employee_value = employee_combobox.get().strip()

            if not all([child_name, birth_year, gender, employee_value]):
                messagebox.showwarning("Предупреждение", "Заполните все поля.")
                return

            if not birth_year.isdigit():
                messagebox.showwarning("Предупреждение", "Год рождения должен быть числом.")
                return

            birth_year_int = int(birth_year)
            if birth_year_int < 2000 or birth_year_int > 2100:
                messagebox.showwarning("Предупреждение", "Введите корректный год рождения.")
                return

            employee_id = employee_map.get(employee_value)
            if employee_id is None:
                messagebox.showwarning("Предупреждение", "Выберите корректного сотрудника.")
                return

            connection = get_connection()

            if connection is None:
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
                return

            try:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE children
                    SET
                        child_name = %s,
                        birth_year = %s,
                        gender = %s,
                        employee_id = %s
                    WHERE birth_certificate_number = %s
                """, (
                    child_name,
                    birth_year_int,
                    gender,
                    employee_id,
                    int(current_birth_certificate_number),
                ))

                connection.commit()
                cursor.close()

                messagebox.showinfo("Успех", "Данные о ребенке успешно изменены.")
                edit_window.destroy()
                self.load_children()

            except Exception as error:
                messagebox.showerror("Ошибка", f"Не удалось изменить данные ребенка:\n{error}")

            finally:
                close_connection(connection)

        tk.Button(
            edit_window,
            text="Сохранить",
            font=("Arial", 11),
            width=16,
            command=update_child
        ).pack(pady=(20, 5))

        tk.Button(
            edit_window,
            text="Отмена",
            font=("Arial", 11),
            width=16,
            command=edit_window.destroy
        ).pack(pady=5)