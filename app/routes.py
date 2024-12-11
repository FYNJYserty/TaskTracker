from app.forms import RegistrationForm, EditUserForm
from app import app
from flask import render_template, redirect, flash, url_for, request
import psycopg

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

def test_connection():
    con = None
    try:
        con = psycopg.connect(host=app.config['DB_SERVER'],
                                user=app.config['DB_USER'],
                                password=app.config['DB_PASSWORD'],
                                dbname=app.config['DB_NAME'])
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    else:
        print(f"Подключение успешно: {con}")
    finally:
        return con