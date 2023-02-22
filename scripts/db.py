import psycopg2
from scripts.config import *


# КЛАСС БАЗЫ ДАННЫХ
class DB:
    # ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ
    def __init__(self):
        self.conn = psycopg2.connect(user=user,
                                     password=password,
                                     host=host,
                                     port=port,
                                     database=database)
        self.cursor = self.conn.cursor()

    # ПРОВЕРКА НАЛИЧИЯ ЛОГИНА
    def login_exists(self, login):
        self.cursor.execute("SELECT * FROM trackers WHERE login = %s", (login,))
        return bool(len(self.cursor.fetchall()))

    # ПРОВЕРКА ПАРОЛЯ
    def check_password(self, login, password_):
        self.cursor.execute("SELECT password FROM trackers WHERE login = %s", (login,))
        return self.cursor.fetchone()[0] == password_

    # ПРОВЕРКА ПАРОЛЯ ДЛЯ УВЕДОМЛЕНИЙ
    def check_password_notification(self, login, password_):
        self.cursor.execute("SELECT password FROM notifications WHERE login = %s", (login,))
        return self.cursor.fetchone()[0] == password_

    # ДОБАВИТЬ АКЦИЮ В ПОРТФЕЛЬ
    def add_stock(self, login, password_, name, country_):
        self.cursor.execute("INSERT INTO trackers (login, password, case_, country) VALUES "
                            "(%s, %s, %s, %s)", (login, password_, name, country_))
        return self.conn.commit()

    # ДОБАВИТЬ УВЕДОМЛЕНИЕ
    def add_notification(self, login, password_, notification, datetime):
        self.cursor.execute("INSERT INTO notifications (login, password, notification, datetime) VALUES "
                            "(%s, %s, %s, %s)", (login, password_, notification, datetime))
        return self.conn.commit()

    # ПРОВЕРИТЬ НАЛИЧИЕ ЛОГИНА ДЛЯ УВЕДОМЛЕНИЙ
    def login_exists_notification(self, login):
        self.cursor.execute("SELECT * FROM notifications WHERE login = %s", (login,))
        return bool(len(self.cursor.fetchall()))

    # ПОЛУЧИТЬ СПИСОК ЛОГИНОВ
    def get_logins(self):
        self.cursor.execute("SELECT login FROM trackers")
        return [i[0] for i in self.cursor.fetchall()]

    # ПОЛУЧИТЬ СПИСОК ЛОГИНОВ ДЛЯ УВЕДОМЛЕНИЙ
    def get_logins_notification(self):
        self.cursor.execute("SELECT login FROM notifications")
        return [i[0] for i in self.cursor.fetchall()]

    # ПОЛУЧИТЬ УВЕДОМЛЕНИЕ
    def get_notifications(self, login):
        self.cursor.execute("SELECT notification, datetime FROM notifications WHERE login = %s", (login,))
        return [[i[0], i[1]] for i in self.cursor.fetchall()]

    # УДАЛИТЬ АКЦИЮ ИЗ ПОРТФЕЛЯ
    def delete_stonk(self, login, name):
        self.cursor.execute("""DELETE from trackers WHERE login = %s AND case_ = %s""", (login, name,))
        return self.conn.commit()

    # УДАЛИТЬ УВЕДОМЛЕНИЕ
    def delete_notification(self, login, datetime):
        self.cursor.execute("""DELETE from notifications WHERE login = %s AND datetime = %s""", (login, datetime,))
        return self.conn.commit()

    # ОЧИСТИТЬ ТАБЛИЦУ С УВЕДОМЛЕНИЯМИ
    def delete_all_notification(self, login):
        self.cursor.execute("""DELETE from notifications WHERE login = %s""", (login,))
        return self.conn.commit()

    # ПОЛУЧИТЬ СПИСОК АКЦИЙ ИЗ ПОТФЕЛЯ
    def get_case(self, login):
        self.cursor.execute("SELECT case_, country FROM trackers WHERE login = %s", (login,))
        return self.cursor.fetchall()

    # СОЗДАТЬ ТАБЛИЦЫ
    def create_table(self):
        try:
            # SQL-запрос для создания новой таблицы
            create_table_query = '''CREATE TABLE trackers
                                  (LOGIN          TEXT,
                                  PASSWORD       TEXT,
                                  CASE_         TEXT,
                                  COUNTRY        TEXT);'''

            create_table_query1 = '''CREATE TABLE notifications
                                  (LOGIN          TEXT,
                                  PASSWORD       TEXT,
                                  NOTIFICATION        TEXT,
                                  DATETIME        TIMESTAMP);'''
            # Выполнение команды: это создает новую таблицу
            self.cursor.execute(create_table_query1)
            self.cursor.execute(create_table_query)
            # self.cursor.execute("""ALTER TABLE trackers ADD COLUMN country TEXT;""")
            # self.cursor.execute("""DELETE from trackers""")
            # self.cursor.execute("""ALTER TABLE trackers RENAME COLUMN case_ TO name;""")
            self.conn.commit()
            print(546)
        except (Exception, psycopg2.Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if self.conn:
                self.cursor.close()
                self.conn.close()
        print("Соединение с PostgreSQL закрыто")


if __name__ == '__main__':
    db = DB()
