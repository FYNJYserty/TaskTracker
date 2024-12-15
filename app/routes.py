from app.forms import RegistrationForm, EditUserForm, LoginForm
from app import app
from app.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_user, login_required, logout_user
import psycopg

@app.route('/info')
@app.route('/')
def info():
    return render_template('info.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        # Данные пользователя
        username = reg_form.username.data
        password_hash = generate_password_hash(reg_form.password.data)
        name = reg_form.name.data
        age = reg_form.age.data
        # Подключение к базе данных
        with psycopg.connect(host=app.config['DB_SERVER'],
                                user=app.config['DB_USER'],
                                password=app.config['DB_PASSWORD'],
                                dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            # Добавляем пользователя в базу данных
            cur.execute('INSERT INTO "user_tt" (username, usr_password, first_name, age) '
                        'VALUES (%s, %s, %s, %s)', (username, password_hash, name, age))
            con.commit()
        # Вывод сообщения
        flash(f'Регистрация {reg_form.username.data} успешна', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=reg_form)

@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/edituser/<string:username>', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    # Проверка прав доступа
    if username != current_user.username and not current_user.is_admin:
        flash('У вас нет прав для редактирования этого пользователя.', 'danger')
        return redirect(url_for('index'))
    with psycopg.connect(host=app.config['DB_SERVER'],
                                user=app.config['DB_USER'],
                                password=app.config['DB_PASSWORD'],
                                dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        password, name, age = cur.execute('SELECT usr_password, first_name, age '
                                            'FROM "user_tt" '
                                            'WHERE username = %s', (username,)).fetchone()
    form = EditUserForm(password=password, name=name, age=age)
    if form.validate_on_submit():
        # Сохранение новых данных пользователя в базе данных
        # Данные пользователя
        new_password_hash = generate_password_hash(form.password.data)
        new_name = form.name.data
        new_age = form.age.data
        # Подключение к базе данных
        with psycopg.connect(host=app.config['DB_SERVER'],
                                user=app.config['DB_USER'],
                                password=app.config['DB_PASSWORD'],
                                dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            # Добавляем пользователя в базу данных
            cur.execute('UPDATE "user_tt"'
                        'SET usr_password = %s, first_name = %s, age = %s'
                        'WHERE username = %s', (new_password_hash, new_name, new_age, username))
            con.commit()
        flash(f'Изменения для пользователя с логином {username} успешно сохранены', 'success')
        return redirect(url_for('edit_user', username=username))
    return render_template('edit_user.html', title='Редактирование пользователя', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        with psycopg.connect(host=app.config['DB_SERVER'],
                                user=app.config['DB_USER'],
                                password=app.config['DB_PASSWORD'],
                                dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            res = cur.execute('SELECT username, usr_password '
                              'FROM "user_tt" '
                              'WHERE username = %s', (login_form.username.data,)).fetchone()
        if res is None or not check_password_hash(res[1], login_form.password.data):
            flash('Попытка входа неудачна', 'danger')
            return redirect(url_for('login'))
        username, password = res
        user = User(username, password)
        login_user(user, remember=login_form.remember_me.data)
        flash(f'Вы успешно вошли в систему, {current_user.username}', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=login_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('info'))

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