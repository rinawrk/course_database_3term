import mysql.connector
from mysql.connector import Error

from app.config import DB_CONFIG


def get_connection():
    """
    Создает и возвращает подключение к базе данных MySQL.
    Если подключиться не удалось, возвращает None.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as error:
        print(f"Ошибка подключения к базе данных: {error}")
        return None


def close_connection(connection):
    """
    Безопасно закрывает подключение к базе данных,
    если оно было успешно создано.
    """
    if connection is not None and connection.is_connected():
        connection.close()