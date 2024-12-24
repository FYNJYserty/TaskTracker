from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeField, StringField, DateField, IntegerField, SelectField, SubmitField, PasswordField, TextAreaField, validators

# Форма регистрации
class RegistrationForm(FlaskForm):
    username = StringField('Логин пользователя', [validators.InputRequired(), validators.Length(min=4, max=25)]) # Логин
    password = PasswordField('Пароль', [validators.InputRequired(), validators.Length(min=6, max=100)]) # Пароль
    name = StringField('Имя пользователя', [validators.Length(min=4, max=50)]) # Имя
    age = IntegerField('Возраст', [validators.InputRequired()]) # Возраст
    submit = SubmitField('Зарегистрироваться') # Кнопка подтверждения
# Форма редактирования пользователя
class EditUserForm(FlaskForm):
    password = PasswordField('Пароль', [validators.InputRequired(), validators.Length(min=6, max=100)]) # Пароль
    name = StringField('Имя пользователя', [validators.Length(min=4, max=50)]) # Имя
    age = IntegerField('Возраст', [validators.InputRequired()]) # Возраст
    submit = SubmitField('Сохранить') # Кнопка подтверждения
# Форма входа пользователя в систему
class LoginForm(FlaskForm):
    username = StringField('Логин', [validators.InputRequired()]) # Логин
    password = PasswordField('Пароль', [validators.InputRequired()]) # Пароль
    remember_me = BooleanField('Запомнить меня') # Флаг
    submit = SubmitField('Войти') # Кнопка подтверждения
# Форма создания организации
class CreateOrganizationForm(FlaskForm):
    name = StringField('Название организации', [validators.InputRequired()]) # Название
    password = PasswordField('Пароль для вступления', [validators.InputRequired()]) # Пароль
    description = StringField('Описание', [validators.InputRequired()]) # Описание
    submit = SubmitField('Создать организацию') # Кнопка подтверждения
# Форма входа пользователя в организацию
class EnterOrganizationForm(FlaskForm):
    name = SelectField('Название организации', choices=[]) # Название
    password = PasswordField('Пароль для вступления', [validators.InputRequired()]) # Пароль
    role = SelectField('Ваша роль', choices=[('Developer', 'Разработчик'), ('Assistant', 'Ассистент'), ('Researcher', 'Исследователь'),
                                            ('Content Creator', 'Создатель контента'), ('Other', 'Другое')]) # Роль пользователя в организации
    submit = SubmitField('Войти в организацию') # Кнопка подтверждения
# Форма редактирования организации
class EditOrganizationForm(FlaskForm):
    name = StringField('Название организации', [validators.InputRequired()]) # Название
    password = PasswordField('Пароль для вступления', [validators.InputRequired()]) # Паоль
    description = StringField('Описание', [validators.InputRequired()]) # Описание
# Форма создания проекта
class CreateProjectForm(FlaskForm):
    org_choice = SelectField('Выберите организацию', choices=[]) # Список организаций
    user_proj = SelectField('Ответственный за проект', choices=[]) # Список пользователей
    name = StringField('Название проекта', [validators.InputRequired()]) # Название
    submit = SubmitField('Создать проект') # Кнопка подтверждения
# Форма создания задачи
class CreateTaskForm(FlaskForm):
    to_user = SelectField('Исполнитель', choices=[]) # Логин исполнителя
    task_name = StringField('Название задачи', [validators.InputRequired()]) # Название
    task_description = TextAreaField('Описание задачи', [validators.InputRequired()]) # Описание
    task_control_date = StringField('Дата дедлайна', [validators.InputRequired()]) # Дедлайн
    project_id = SelectField('ID проекта', choices=[]) # Id проекта
    task_status = BooleanField('Статус') # Статус задачи
    submit = SubmitField('Создать задачу') # Кнопка подтверждения
# Форма изменения задачи
class EditTaskForm(FlaskForm):
    to_user = SelectField('Исполнитель', choices=[]) # Логин пользователя
    task_name = StringField('Название задачи', [validators.InputRequired()]) # Название
    task_description = TextAreaField('Описание задачи', [validators.InputRequired()]) # Описание
    task_control_date = StringField('Дата дедлайна', [validators.InputRequired()]) # Дедлайн
    task_status = BooleanField('Статус') # Статус задачи
    submit = SubmitField('Изменить задачу') # Кнопка подтверждения
