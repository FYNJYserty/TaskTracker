import os
from dotenv import load_dotenv

load_dotenv()
# Конфигурация базы данных
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abcde'
    DB_SERVER = os.environ.get('DB_SERVER') or 'localhost'
    DB_USER = os.environ.get('DB_USER') or 'postgres'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'your_password'
    DB_NAME = os.environ.get('DB_NAME') or 'your_db_name'
    DB_PORT = os.environ.get('DB_PORT') or 'your_db_port'