import tkinter as tk

from app.gui.main_window import MainWindow


def main():
    """
    Точка входа в приложение.
    Создает и запускает главное окно Tkinter.
    """
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()