import tkinter as tk
from tkinter import ttk, messagebox

from app.db import get_connection, close_connection


class DepartmentsWindow:
    """
    Окно раздела 'Отделы'.

    В этом окне отображается список отделов из базы данных.
    Реализованы:
    - просмотр списка;
    - добавление нового отдела;
    - редактирование выбранного отдела;
    - удаление отдела.
    """

    def __init__(self, parent):
        # Создаем отдельное дочернее окно.
        self.window = tk.Toplevel(parent)
        self.window.title("Отделы")
        self.window.geometry("900x520")
        self.window.minsize(760, 420)

        # Таблица с данными отделов.
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

        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=(0, 15))

        add_button = tk.Button(
            buttons_frame,
            text="Добавить отдел",
            font=("Arial", 11),
            width=18,
            command=self.open_add_department_window
        )
        add_button.grid(row=0, column=0, padx=8)

        edit_button = tk.Button(
            buttons_frame,
            text="Изменить отдел",
            font=("Arial", 11),
            width=18,
            command=self.open_edit_department_window
        )
        edit_button.grid(row=0, column=1, padx=8)

        delete_button = tk.Button(
            buttons_frame,
            text="Удалить отдел",
            font=("Arial", 11),
            width=18,
            command=self.delete_department
        )
        delete_button.grid(row=0, column=2, padx=8)

        refresh_button = tk.Button(
            buttons_frame,
            text="Обновить список",
            font=("Arial", 11),
            width=18,
            command=self.load_departments
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

        table_frame = tk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tree = ttk.Treeview(
            table_frame,
            columns=("department_id", "department_name"),
            show="headings"
        )

        self.tree.heading("department_id", text="Номер отдела")
        self.tree.heading("department_name", text="Название отдела")

        self.tree.column("department_id", width=150, anchor="center")
        self.tree.column("department_name", width=550, anchor="w")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

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
            cursor.execute("""
                SELECT department_id, department_name
                FROM departments
                ORDER BY department_id
            """)
            rows = cursor.fetchall()

            # Полностью очищаем таблицу перед новой загрузкой.
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Заполняем таблицу отделами из базы данных.
            for row in rows:
                self.tree.insert("", "end", values=row)

            cursor.close()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось загрузить отделы:\n{error}")

        finally:
            close_connection(connection)

    def open_add_department_window(self):
        """
        Открывает окно для добавления нового отдела.
        """
        add_window = tk.Toplevel(self.window)
        add_window.title("Добавление отдела")
        add_window.geometry("400x280")
        add_window.resizable(True, True)

        tk.Label(
            add_window,
            text="Номер отдела:",
            font=("Arial", 11)
        ).pack(pady=(20, 5))

        department_id_entry = tk.Entry(add_window, font=("Arial", 11), width=30)
        department_id_entry.pack(pady=5)

        tk.Label(
            add_window,
            text="Название отдела:",
            font=("Arial", 11)
        ).pack(pady=(15, 5))

        department_name_entry = tk.Entry(add_window, font=("Arial", 11), width=30)
        department_name_entry.pack(pady=5)

        def save_department():
            """
            Сохраняет новый отдел в базу данных.
            """
            department_id = department_id_entry.get().strip()
            department_name = department_name_entry.get().strip()

            if not department_id or not department_name:
                messagebox.showwarning("Предупреждение", "Заполните все поля.")
                return

            if not department_id.isdigit():
                messagebox.showwarning("Предупреждение", "Номер отдела должен быть числом.")
                return

            connection = get_connection()

            if connection is None:
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
                return

            try:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO departments (department_id, department_name)
                    VALUES (%s, %s)
                """, (int(department_id), department_name))
                connection.commit()
                cursor.close()

                messagebox.showinfo("Успех", "Отдел успешно добавлен.")
                add_window.destroy()
                self.load_departments()

            except Exception as error:
                messagebox.showerror("Ошибка", f"Не удалось добавить отдел:\n{error}")

            finally:
                close_connection(connection)

        tk.Button(
            add_window,
            text="Сохранить",
            font=("Arial", 11),
            width=15,
            command=save_department
        ).pack(pady=(20, 5))

        tk.Button(
            add_window,
            text="Отмена",
            font=("Arial", 11),
            width=15,
            command=add_window.destroy
        ).pack(pady=5)

    def open_edit_department_window(self):
        """
        Открывает окно редактирования выбранного отдела.
        """
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Сначала выберите отдел в таблице.")
            return

        values = self.tree.item(selected_item[0], "values")
        department_id = values[0]
        current_department_name = values[1]

        edit_window = tk.Toplevel(self.window)
        edit_window.title("Редактирование отдела")
        edit_window.geometry("400x280")
        edit_window.resizable(True, True)

        tk.Label(
            edit_window,
            text="Номер отдела:",
            font=("Arial", 11)
        ).pack(pady=(20, 5))

        department_id_entry = tk.Entry(edit_window, font=("Arial", 11), width=30)
        department_id_entry.pack(pady=5)
        department_id_entry.insert(0, str(department_id))
        department_id_entry.config(state="disabled")

        tk.Label(
            edit_window,
            text="Название отдела:",
            font=("Arial", 11)
        ).pack(pady=(15, 5))

        department_name_entry = tk.Entry(edit_window, font=("Arial", 11), width=30)
        department_name_entry.pack(pady=5)
        department_name_entry.insert(0, current_department_name)

        def update_department():
            """
            Обновляет название выбранного отдела.
            """
            new_department_name = department_name_entry.get().strip()

            if not new_department_name:
                messagebox.showwarning("Предупреждение", "Введите название отдела.")
                return

            connection = get_connection()

            if connection is None:
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
                return

            try:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE departments
                    SET department_name = %s
                    WHERE department_id = %s
                """, (new_department_name, int(department_id)))
                connection.commit()
                cursor.close()

                messagebox.showinfo("Успех", "Отдел успешно изменен.")
                edit_window.destroy()
                self.load_departments()

            except Exception as error:
                messagebox.showerror("Ошибка", f"Не удалось изменить отдел:\n{error}")

            finally:
                close_connection(connection)

        tk.Button(
            edit_window,
            text="Сохранить",
            font=("Arial", 11),
            width=15,
            command=update_department
        ).pack(pady=(20, 5))

        tk.Button(
            edit_window,
            text="Отмена",
            font=("Arial", 11),
            width=15,
            command=edit_window.destroy
        ).pack(pady=5)

    def delete_department(self):
        """
        Удаляет выбранный отдел из базы данных.

        Перед удалением проверяется:
        1. выбран ли отдел;
        2. нет ли у отдела связанных сотрудников.
        """
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Сначала выберите отдел в таблице.")
            return

        values = self.tree.item(selected_item[0], "values")
        department_id = int(values[0])
        department_name = values[1]

        confirm = messagebox.askyesno(
            "Подтверждение",
            f"Удалить отдел '{department_name}'?"
        )

        if not confirm:
            return

        connection = get_connection()

        if connection is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            return

        try:
            cursor = connection.cursor()

            # Проверяем, есть ли у отдела сотрудники.
            cursor.execute("""
                SELECT COUNT(*)
                FROM employees
                WHERE department_id = %s
            """, (department_id,))
            employees_count = cursor.fetchone()[0]

            if employees_count > 0:
                messagebox.showwarning(
                    "Предупреждение",
                    "Нельзя удалить отдел, к которому привязаны сотрудники."
                )
                cursor.close()
                return

            # Если связанных сотрудников нет, удаляем отдел.
            cursor.execute("""
                DELETE FROM departments
                WHERE department_id = %s
            """, (department_id,))
            connection.commit()
            cursor.close()

            messagebox.showinfo("Успех", "Отдел успешно удален.")
            self.load_departments()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось удалить отдел:\n{error}")

        finally:
            close_connection(connection)