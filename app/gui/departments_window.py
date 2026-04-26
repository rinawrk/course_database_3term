import tkinter as tk


class DepartmentsWindow:
    """
    Окно раздела 'Отделы'.
    Пока это заготовка, которую позже заполним таблицей и кнопками CRUD.
    """

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Отделы")
        self.window.geometry("700x500")
        self.window.minsize(600, 400)

        self.create_widgets()

    def create_widgets(self):
        """
        Создает элементы интерфейса окна 'Отделы'.
        """
        title_label = tk.Label(
            self.window,
            text="Раздел: Отделы",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(20, 10))

        info_label = tk.Label(
            self.window,
            text="Здесь будет таблица отделов и кнопки добавления, редактирования и удаления.",
            font=("Arial", 11),
            wraplength=500,
            justify="center"
        )
        info_label.pack(pady=(0, 20))

        close_button = tk.Button(
            self.window,
            text="Закрыть",
            font=("Arial", 11),
            width=15,
            command=self.window.destroy
        )
        close_button.pack(pady=10)