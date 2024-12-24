import psycopg
from app import app
from app import login_manager
from flask_login import UserMixin
# Создание класса пользователя
class User(UserMixin):
    # Инициализация пользователя (Конструктор)
    def __init__(self, username, password):
        self.username = username
        self.password = password
    # Переопределение метода получения ID
    def get_id(self):
        return self.username  # Используем username в качестве уникального идентификатора
# Загрузка пользователя
@login_manager.user_loader
def load_user(username):
    with psycopg.connect(host=app.config['DB_SERVER'],
                                user=app.config['DB_USER'],
                                password=app.config['DB_PASSWORD'],
                                dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        username, password = cur.execute('SELECT username, usr_password '
                                         'FROM "user_tt" '
                                         'WHERE username = %s', (username,)).fetchone()
    return User(username, password)