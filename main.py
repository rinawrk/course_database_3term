from app.db import get_connection, close_connection


def main():
    """
    Точка входа в программу.
    Пока просто проверяем, что Python-приложение может подключиться к MySQL.
    """
    connection = get_connection()

    if connection is None:
        print("Не удалось подключиться к базе данных.")
        return

    print("Подключение к базе данных выполнено успешно.")

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()

        print("Текущая база данных:", result[0])
        cursor.close()
    finally:
        close_connection(connection)


if __name__ == "__main__":
    main()