import sqlite3


def read_users_db():
    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Выполняем запрос на извлечение всех данных из таблицы users
        cursor.execute("SELECT * FROM users")

        # Получаем все результаты запроса
        rows = cursor.fetchall()

        # Обрабатываем и выводим результаты
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print(f"Ошибка при работе с SQLite: {e}")
    finally:
        # Закрываем соединение
        if conn:
            conn.close()


# Вызов функции для чтения данных
read_users_db()