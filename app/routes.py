from app.forms import *
from app import app
from app.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort, make_response, render_template, redirect, flash, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from urllib.parse import quote
import psycopg

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_404.html'), 404

@app.errorhandler(401)
def page_not_found(error):
    return render_template('error_401.html'), 401

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
        cur.close()
        con.close()
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
    cur.close()
    con.close()
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
            # Меняем данные пользователя
            cur.execute('UPDATE "user_tt"'
                        'SET usr_password = %s, first_name = %s, age = %s'
                        'WHERE username = %s', (new_password_hash, new_name, new_age, username))
            con.commit()
        cur.close()
        con.close()
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
        cur.close()
        con.close()
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

@app.route('/index/create_organization', methods=['GET', 'POST'])
def create_organization():
    create_organization_form = CreateOrganizationForm()
    if create_organization_form.validate_on_submit():
        # Данные организации
        org_name = create_organization_form.name.data
        org_password = generate_password_hash(create_organization_form.password.data)
        org_description = create_organization_form.description.data
        with psycopg.connect(host=app.config['DB_SERVER'],
                                user=app.config['DB_USER'],
                                password=app.config['DB_PASSWORD'],
                                dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            # Добавляем организацию в базу данных и получаем её идентификатор
            cur.execute('INSERT INTO organization (org_name, org_password, description) '
                        'VALUES (%s, %s, %s) RETURNING org_id', (org_name, org_password, org_description))
            org_id = cur.fetchone()[0]
            # Добавляем пользователя в статусы организации
            cur.execute('INSERT INTO user_status (username, organization_id, usr_position) '
                        'VALUES (%s, %s, %s)', (current_user.username, org_id, 'Owner'))
            con.commit()
        cur.close()
        con.close()
        flash(f'Организация {org_name} успешно создана', 'success')
        return redirect((url_for('index')))
    return render_template('create_organization.html', title='Создать организацию', form=create_organization_form)

@app.route('/index/enter_organization', methods=['GET', 'POST'])
def enter_organization():
    enter_organization_form = EnterOrganizationForm()

    # Подключение к базе данных
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        # Проверка существования организации и получения хеша пароля
        cur.execute("""
            SELECT org_name
            FROM organization
        """)
        orgs = cur.fetchall()
        org_choices = [(org[0], org[0]) for org in orgs]  # Список организаций для выпадающего списка
        enter_organization_form.name.choices = org_choices
    cur.close()
    con.close()
    if enter_organization_form.validate_on_submit():
        org_name = enter_organization_form.name.data
        org_password = enter_organization_form.password.data
        org_role = enter_organization_form.role.data

        # Подключение к базе данных
        with psycopg.connect(host=app.config['DB_SERVER'],
                            user=app.config['DB_USER'],
                            password=app.config['DB_PASSWORD'],
                            dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            # Проверка существования организации и получения хеша пароля
            cur.execute("""
                SELECT org_id, org_password
                FROM organization
                WHERE org_name = %s
            """, (org_name,))
            org = cur.fetchone()
            if org and check_password_hash(org[1], org_password):  # Проверка хеша пароля
                org_id = org[0]
                username = current_user.username  # Предполагается, что пользователь уже аутентифицирован
                # Добавление пользователя в организацию
                cur.execute("""
                    INSERT INTO user_status (username, organization_id, usr_position)
                    VALUES (%s, %s, %s)
                """, (username, org_id, org_role))
                con.commit()
                flash('Вы успешно вошли в организацию!', 'success')
                return redirect(url_for('index'))  # Перенаправление на главную страницу
            else:
                flash('Неверное название организации или пароль.', 'danger')
    return render_template('enter_organization.html', title='Войти в организацию', form=enter_organization_form)

@app.route('/index/view_organization', methods=['GET', 'POST'])
def view_organization():
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        cur.execute("SELECT first_name FROM user_tt WHERE username = %s", (current_user.username,))
        user_name = cur.fetchone()[0]

        # Получение всех оганизаций, где пользователь владелец
        cur.execute("""
            SELECT *
            FROM organization o
            JOIN user_status us ON us.organization_id = o.org_id
            WHERE us.username = %s AND us.usr_position = 'Owner'
        """, (current_user.username,))
        organizations = cur.fetchall()
        
        # Преобразуем кортежи в словари для удобства
        organizations_list = []
        for org in organizations:
            organizations_list.append({
                'org_id': org[0],
                'org_name': org[1],
                'org_description': org[3]
            })
        
        # Получение всех оганизаций, где пользователь участник
        cur.execute("""
            SELECT *
            FROM organization o
            JOIN user_status us ON us.organization_id = o.org_id
            WHERE us.username = %s AND us.usr_position <> 'Owner'
        """, (current_user.username,))
        organizations2 = cur.fetchall()
        
        # Преобразуем кортежи в словари для удобства
        organizations_list2 = []
        for org in organizations2:
            organizations_list2.append({
                'org_id': org[0],
                'org_name': org[1],
                'org_description': org[3]
            })
    cur.close()
    con.close()
    return render_template('view_organization.html', title='Список организаций', organizations=organizations_list, username=user_name, organizations2=organizations_list2)

@app.route('/index/organization_details/<int:org_id>', methods=['GET', 'POST'])
def organization_details(org_id):
    # Подключение к базе данных
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        name, description = cur.execute("""
            SELECT org_name, description
            FROM organization
            WHERE org_id = %s
        """, (org_id,)).fetchone()

        cur.execute("""
            SELECT username, usr_position
            FROM user_status
            WHERE organization_id = %s AND usr_position <> 'Owner'
        """, (org_id,))
        members = cur.fetchall()

        members_list = []
        for member in members:
            members_list.append({
                'username': member[0],
                'usr_position': member[1]
            })
    
        edit_org_form = EditOrganizationForm(name=name, description=description)

        if edit_org_form.validate_on_submit():
            org_name = edit_org_form.name.data
            org_password = generate_password_hash(edit_org_form.password.data)
            org_description = edit_org_form.description.data
            cur.execute("""
                UPDATE organization
                SET org_name = %s, org_password = %s, description = %s
                WHERE org_id = %s
            """, (org_name, org_password, org_description, org_id))
            con.commit()
            flash('Организация успешно изменена!','success')
            return redirect(url_for('organization_details', org_id=org_id))
    cur.close()
    con.close()
    return render_template('organization_details.html', form=edit_org_form, title='Детали организации', members=members_list, org_id=org_id)

@app.route('/index/create_project', methods=['GET', 'POST'])
def create_project():
    # Инициализация формы
    create_project_form = CreateProjectForm()

    # Подключение к базе данных
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()

        # Получение организаций
        cur.execute("""
            SELECT org_id, org_name
            FROM organization
            WHERE org_id IN (
                SELECT organization_id
                FROM user_status
                WHERE username = %s AND usr_position = %s
            )
        """, (current_user.username, 'Owner'))
        orgs = cur.fetchall()
        org_choices = [(org[0], org[1]) for org in orgs]
        create_project_form.org_choice.choices = org_choices

        # Получение всех пользователей
        cur.execute("""
            SELECT DISTINCT u.username
            FROM user_tt u
            JOIN user_status us ON u.username = us.username
            WHERE us.organization_id IN (
                SELECT organization_id
                FROM user_status
                WHERE username = %s AND usr_position = %s
            )
        """, (current_user.username, 'Owner'))
        users = cur.fetchall()
        user_choices = [(user[0], user[0]) for user in users]
        create_project_form.user_proj.choices = user_choices

        if request.method == 'POST':
            selected_org_id = create_project_form.org_choice.data
            selected_user = create_project_form.user_proj.data

            # Проверяем, что выбранный пользователь принадлежит выбранной организации
            cur.execute("""
                SELECT COUNT(*)
                FROM user_status
                WHERE username = %s AND organization_id = %s
            """, (selected_user, selected_org_id))
            count = cur.fetchone()[0]
            if count == 0:
                flash('Выбранный пользователь не принадлежит к выбранной организации.', 'danger')
            else:
                # Проверяем, валидируется ли форма
                if create_project_form.validate_on_submit():
                    proj_name = create_project_form.name.data
                    
                    # Вставляем новый проект в базу данных
                    cur.execute("""
                        INSERT INTO project (organization_id, username, proj_name)
                        VALUES (%s, %s, %s)
                    """, (selected_org_id, selected_user, proj_name))
                    con.commit()
                    flash('Проект успешно создан!', 'success')
                    return redirect(url_for('index'))
        cur.close()
        con.close()

    return render_template('create_project.html', title='Создать проект', form=create_project_form)

@app.route('/index/create_task', methods=['GET', 'POST'])
def create_task():
    # Инициализация формы
    create_task_form = CreateTaskForm()

    # Подключение к базе данных
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        # Получение проектов, в которых участвует пользователь
        cur.execute("""
            SELECT p.proj_id, p.proj_name
            FROM project p
            JOIN organization o ON p.organization_id = o.org_id
            JOIN user_status us ON o.org_id = us.organization_id
            WHERE us.username = %s AND us.usr_position = 'Owner'
            
            UNION
            
            SELECT p.proj_id, p.proj_name
            FROM project p
            WHERE username=%s
        """, (current_user.username, current_user.username))
        projects = cur.fetchall()
        usr_projects = [(proj[0], proj[1]) for proj in projects]
        create_task_form.project_id.choices = usr_projects
        
        # Получение списка людей
        cur.execute("""
            SELECT u.username
            FROM user_tt u
            JOIN user_status us ON u.username = us.username
            WHERE us.organization_id IN (
                SELECT organization_id
                FROM user_status
                WHERE username = %s AND usr_position = %s
            )

            UNION

            SELECT us.username
            FROM user_status us
            WHERE us.organization_id IN (
                SELECT p.organization_id
                FROM project p
                WHERE p.username = %s
            )
        """, (current_user.username, 'Owner', current_user.username))
        users = cur.fetchall()
        to_user = [(user[0]) for user in users]
        create_task_form.to_user.choices = to_user

        if request.method == 'POST':
            selected_user = create_task_form.to_user.data
            selected_proj_id = create_task_form.project_id.data
            
            # Проверяем, что выбранный пользователь принадлежит выбранной организации
            cur.execute("""
                SELECT COUNT(*)
                FROM user_status
                WHERE username = %s AND organization_id IN (
                    SELECT organization_id
                    FROM project
                    WHERE proj_id = %s
                )
            """, (selected_user, selected_proj_id))
            count = cur.fetchone()[0]
            if count == 0:
                flash('Выбранный пользователь не принадлежит к выбранной организации.', 'danger')
            else:
                # Проверяем, валидируется ли форма
                if create_task_form.validate_on_submit():
                    task_name = create_task_form.task_name.data
                    task_description = create_task_form.task_description.data
                    task_date = create_task_form.task_control_date.data
                    task_status = create_task_form.task_status.data
                    
                    # Вставляем новый проект в базу данных
                    cur.execute("""
                        INSERT INTO task (tsk_username, tsk_name, description, deadline, status, project_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (selected_user, task_name, task_description, task_date, task_status, selected_proj_id))
                    con.commit()
                    flash('Задача успешно создана!', 'success')
                    return redirect(url_for('index'))
    cur.close()
    con.close()
    return render_template('create_task.html', title='Создать задачу', form=create_task_form)

@app.route('/index/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # Проверка на права доступа для удаления задачи
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        # Получение id проекта
        proj_id = cur.execute("""
            SELECT project_id
            FROM task
            WHERE tsk_id = %s
        """,(task_id,)).fetchone()[0]
        # Получение логина пользователя, ответственного за проект
        usr_project = cur.execute("""
            SELECT username
            FROM project
            WHERE proj_id = %s
        """, (proj_id,)).fetchone()[0]
        # Получение логина пользователя, ответственного за организацию
        usr_org = cur.execute("""
            SELECT username
            FROM user_status
            WHERE usr_position = 'Owner' AND organization_id IN (
                SELECT organization_id
                FROM project
                WHERE proj_id = %s
            )""", (proj_id,)).fetchone()[0]
        # Проверка, может ли текущий пользователь редактировать проект
        if current_user.username != usr_org:
            if current_user.username != usr_project:
                flash('У пользователя нет прав на данное действие', 'danger')
                return redirect(url_for('view_tasks'))
    cur.close()
    con.close()

    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        # Получение текущей информации о задаче
        to_user, task_name, task_description, task_control_date, task_status = cur.execute("""
            SELECT tsk_username, tsk_name, description, deadline, status
            FROM task
            WHERE tsk_id = %s
        """, (task_id, )).fetchone()
    # Инициализация формы
    edit_task_form = EditTaskForm(to_user=to_user,
                                    task_name=task_name,
                                    task_description=task_description,
                                    task_control_date=task_control_date,
                                    task_status=task_status)
    # Подключение к базе данных
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        # Получение Id организации
        org_id = cur.execute("""
            SELECT organization_id
            FROM project
            WHERE proj_id IN (
                SELECT project_id
                FROM task
                WHERE tsk_id = %s)
        """, (task_id,)).fetchone()[0]

        # Получение списка людей
        cur.execute("""
            SELECT us.username
            FROM user_status us
            WHERE us.organization_id = %s
        """, (org_id,))
        users = cur.fetchall()
        to_user = [(user[0]) for user in users]
        edit_task_form.to_user.choices = to_user

        # Проверяем, валидируется ли форма
        if edit_task_form.validate_on_submit():
            selected_user = edit_task_form.to_user.data
            task_name = edit_task_form.task_name.data
            task_description = edit_task_form.task_description.data
            task_date = edit_task_form.task_control_date.data
            task_status = edit_task_form.task_status.data
                    
            # Обновляем задачу
            cur.execute("""
                UPDATE task
                SET tsk_username = %s, tsk_name = %s, description = %s, deadline = %s, status = %s
                WHERE tsk_id = %s
            """, (selected_user, task_name, task_description, task_date, task_status, task_id))
            con.commit()
            flash('Задача успешно изменена!', 'success')
            return redirect(url_for('view_tasks'))
    cur.close()
    con.close()
    return render_template('create_task.html', title='Изменить задачу', form=edit_task_form)

@app.route('/index/view_tasks')
def view_tasks():
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        
        # Получение имени текущего пользователя
        cur.execute("SELECT first_name FROM user_tt WHERE username = %s", (current_user.username,))
        user_name = cur.fetchone()[0]
        
        # Получение всех проектов текущего пользователя
        cur.execute("""
            SELECT p.proj_id, p.organization_id, p.username, p.proj_name
            FROM project p
            JOIN task t ON p.proj_id = t.project_id
            WHERE t.tsk_username = %s
            GROUP BY p.proj_id, p.organization_id, p.username, p.proj_name
        """, (current_user.username,))
        
        projects = cur.fetchall()
        
        # Получение задач для каждого проекта
        projects_with_tasks = []
        for project in projects:
            proj_id, proj_org, proj_usr, proj_name = project
            cur.execute("SELECT org_name FROM organization WHERE org_id = %s", (proj_org,))
            org_name = cur.fetchone()[0]
            # Получение всех задач проекта текущего пользователя
            cur.execute("SELECT * FROM task WHERE project_id = %s AND tsk_username = %s", (proj_id, current_user.username))
            tasks = cur.fetchall()
            
            # Преобразуем кортежи задач в словари
            tasks_list = []
            for task in tasks:
                tasks_list.append({
                    'tsk_id': task[0],
                    'tsk_username': task[1],
                    'tsk_name': task[2],
                    'description': task[3],
                    'deadline': task[4],
                    'status': task[5],
                    'project_id': task[6]
                })
            
            projects_with_tasks.append({
                'proj_id': proj_id,
                'proj_org': org_name,
                'proj_usr': proj_usr,
                'proj_name': proj_name,
                'tasks': tasks_list
            })
    
    cur.close()
    con.close()
    return render_template('view_tasks.html', projects=projects_with_tasks, user_name=user_name)

@app.route('/task/<int:task_id>')
def task_details(task_id):
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        
        # Получение информации о задаче
        cur.execute("SELECT * FROM task WHERE tsk_id = %s", (task_id,))
        task = cur.fetchone()
        
        if not task:
            flash('Задача не найдена', 'danger')
            return redirect(url_for('view_tasks'))
        # Получение комментариев для задачи
        cur.execute("SELECT * FROM comment_usr WHERE task_id = %s", (task_id,))
        comments = cur.fetchall()

        # Получение вложений для задачи
        cur.execute("SELECT * FROM attachment WHERE task_id = %s", (task_id,))
        attachments = cur.fetchall()
    return render_template('task_details.html', task=task, comments=comments, attachments=attachments)

@app.route('/download_attachment/<int:attachment_id>')
def download_attachment(attachment_id):
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM attachment WHERE attach_id = %s", (attachment_id,))
        attachment = cur.fetchone()
        
        if not attachment:
            # Если вложение не найдено, возвращаем 404 ошибку
            abort(404)

        # Устанавливаем заголовки для скачивания файла
        response = make_response(attachment[4])  # file_data
        response.headers['Content-Type'] = attachment[3]  # mime_type
        encoded_file_name = quote(attachment[5])
        response.headers['Content-Disposition'] = f'attachment; filename={encoded_file_name}'  # attach_username

        return response

@app.route('/task/<int:task_id>/add_attachment', methods=['POST'])
def add_attachment(task_id):
    file = request.files['file']
    attach_username = current_user.username
    mime_type = file.content_type
    file_data = file.read()
    file_name = file.filename
    
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO attachment (attach_username, mime_type, file_data, task_id, file_name) VALUES (%s, %s, %s, %s, %s)",
                    (attach_username, mime_type, file_data, task_id, file_name))
        con.commit()

    flash('Вложение добавлено!', 'success')
    return redirect(url_for('task_details', task_id=task_id))

@app.route('/task/<int:task_id>/add_comment', methods=['POST'])
def add_comment(task_id):
    comment_text = request.form['comment']
    
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO comment_usr (com_username, comment_text, task_id) VALUES (%s, %s, %s)",
                    (current_user.username, comment_text, task_id))
        con.commit()

    flash('Комментарий добавлен!', 'success')
    return redirect(url_for('task_details', task_id=task_id))

@app.route('/task/<int:task_id>/update_status', methods=['POST'])
def update_task_status(task_id):
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        cur.execute("UPDATE task SET status = TRUE WHERE tsk_id = %s", (task_id,))
        con.commit()

    flash('Статус задачи обновлен на "Выполнено"!', 'success')
    return redirect(url_for('task_details', task_id=task_id))

@app.route('/index/other_tasks')
def other_tasks():
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        
        # Получение всех проектов текущего пользователя
        cur.execute("""
            SELECT p.proj_id, p.organization_id, p.username, p.proj_name
            FROM project p
            WHERE p.username = %s

            UNION

            SELECT p.proj_id, p.organization_id, p.username, p.proj_name
            FROM project p
            JOIN user_status us ON us.organization_id = p.organization_id
            WHERE us.username = %s AND us.usr_position = 'Owner'
        """, (current_user.username, current_user.username))
        
        projects = cur.fetchall()
        
        # Получение задач для каждого проекта
        projects_with_tasks = []
        for project in projects:
            proj_id, proj_org, proj_usr, proj_name = project
            cur.execute("SELECT org_name FROM organization WHERE org_id = %s", (proj_org,))
            org_name = cur.fetchone()[0]
            # Получение всех задач проекта текущего пользователя
            cur.execute("SELECT * FROM task WHERE project_id = %s AND tsk_username <> %s", (proj_id, current_user.username))
            tasks = cur.fetchall()
            
            # Преобразуем кортежи задач в словари
            tasks_list = []
            for task in tasks:
                tasks_list.append({
                    'tsk_id': task[0],
                    'tsk_username': task[1],
                    'tsk_name': task[2],
                    'description': task[3],
                    'deadline': task[4],
                    'status': task[5],
                    'project_id': task[6]
                })
            
            projects_with_tasks.append({
                'proj_id': proj_id,
                'proj_org': org_name,
                'proj_usr': proj_usr,
                'proj_name': proj_name,
                'tasks': tasks_list
            })
    
    cur.close()
    con.close()
    return render_template('view_tasks.html', projects=projects_with_tasks, user_name='остальных')

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    # Проверка на права доступа для удаления задачи
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        # Получение id проекта
        proj_id = cur.execute("""
            SELECT project_id
            FROM task
            WHERE tsk_id = %s
        """,(task_id,)).fetchone()[0]
        # Получение логина пользователя, ответственного за проект
        usr_project = cur.execute("""
            SELECT username
            FROM project
            WHERE proj_id = %s
        """, (proj_id,)).fetchone()[0]
        # Получение логина пользователя, ответственного за организацию
        usr_org = cur.execute("""
            SELECT username
            FROM user_status
            WHERE usr_position = 'Owner' AND organization_id IN (
                SELECT organization_id
                FROM project
                WHERE proj_id = %s
            )""", (proj_id,)).fetchone()[0]
        # Проверка, может ли текущий пользователь редактировать проект
        if current_user.username != usr_org:
            if current_user.username != usr_project:
                flash('У пользователя нет прав на данное действие', 'danger')
                return redirect(url_for('view_tasks'))
    cur.close()
    con.close()
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()

        # Удаляем комментарии
        cur.execute("DELETE FROM comment_usr WHERE task_id = %s", (task_id,))
        # Удаляем вложения
        cur.execute("DELETE FROM attachment WHERE task_id = %s", (task_id,))
        # Удаляем задачу
        cur.execute("DELETE FROM task WHERE tsk_id = %s", (task_id,))
        con.commit()
    cur.close()
    con.close()
    flash('Задача успешно удалена!', 'success')
    return redirect(url_for('view_tasks'))

@app.route('/organization_details/<int:org_id>/delete_user/<string:username>', methods=['GET', 'POST'])
def delete_user(org_id, username):
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()

        # Удаляем пользователя из статуса пользователя
        cur.execute("""DELETE
                    FROM user_status
                    WHERE username = %s AND organization_id = %s
        """, (username, org_id))
        con.commit()
    cur.close()
    con.close()
    flash(f'Пользователь {username} успешно удален!', 'success')
    return redirect(url_for('organization_details', org_id=org_id))

@app.route('/view_organization/quit/<int:org_id>', methods=['GET', 'POST'])
def quit(org_id):
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        # Выход пользователя
        cur.execute("""
            DELETE
            FROM user_status
            WHERE organization_id = %s AND username = %s
        """, (org_id, current_user.username))
        con.commit()
    cur.close()
    con.close()
    flash('Вы успешно покинули организацию', 'success')
    return redirect(url_for('view_organization'))

@app.route('/delete_organization/<int:org_id>', methods=['POST'])
def delete_organization(org_id):
    # Подключение к базе данных
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
            
        # Выполнение удаления всех связанных данных
        cur.execute("""
            DELETE
            FROM attachment
            WHERE task_id IN
                (SELECT tsk_id
                FROM task
                WHERE project_id IN
                    (SELECT proj_id
                    FROM project
                    WHERE organization_id = %s));
        """, (org_id,))
            
        cur.execute("""
            DELETE
            FROM comment_usr
            WHERE task_id IN
                (SELECT tsk_id
                FROM task
                WHERE project_id IN
                    (SELECT proj_id
                    FROM project
                    WHERE organization_id = %s));
        """, (org_id,))
            
        cur.execute("""
            DELETE
            FROM task
            WHERE project_id IN
                (SELECT proj_id
                FROM project
                WHERE organization_id = %s);
        """, (org_id,))
            
        cur.execute("""
            DELETE
            FROM project
            WHERE organization_id = %s;
        """, (org_id,))
            
        cur.execute("""
            DELETE
            FROM user_status
            WHERE organization_id = %s;
        """, (org_id,))
            
        cur.execute("""
            DELETE
            FROM organization
            WHERE org_id = %s;
        """, (org_id,))
            
        con.commit()
        flash('Организация успешно удалена.', 'success')
    return redirect(url_for('view_organization'))

@app.route('/delete_project/<int:proj_id>', methods=['GET', 'POST'])
def delete_project(proj_id):
    with psycopg.connect(host=app.config['DB_SERVER'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        
        # Получение логина пользователя, ответственного за проект
        usr_project = cur.execute("""
            SELECT username
            FROM project
            WHERE proj_id = %s
        """, (proj_id,)).fetchone()[0]
        # Получение логина пользователя, ответственного за организацию
        usr_org = cur.execute("""
            SELECT username
            FROM user_status
            WHERE usr_position = 'Owner' AND organization_id IN (
                SELECT organization_id
                FROM project
                WHERE proj_id = %s
            )""", (proj_id,)).fetchone()[0]
        # Проверка, может ли текущий пользователь редактировать проект
        if current_user.username != usr_org:
            if current_user.username != usr_project:
                flash('У пользователя нет прав на данное действие', 'danger')
                return redirect(url_for('view_tasks'))
        
        # Удаляем связанные данные
        cur.execute("""
            DELETE
            FROM attachment
            WHERE task_id IN
                (SELECT tsk_id
                FROM task
                WHERE project_id = %s);
        """, (proj_id,))
            
        cur.execute("""
            DELETE
            FROM comment_usr
            WHERE task_id IN
                (SELECT tsk_id
                FROM task
                WHERE project_id = %s);
        """, (proj_id,))
            
        cur.execute("""
            DELETE
            FROM task
            WHERE project_id = %s;
        """, (proj_id,))
            
        cur.execute("""
            DELETE
            FROM project
            WHERE proj_id = %s;
        """, (proj_id,))
        con.commit()
        flash('Проект успешно удален!', 'success')
    cur.close()
    con.close()
    return redirect(url_for('view_tasks'))