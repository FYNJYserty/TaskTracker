from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, DateField, IntegerField, SelectField, SubmitField, PasswordField, validators

class RegistrationForm(FlaskForm):
    username = StringField('Логин пользователя', [validators.Length(min=4, max=25)]) # Username field
    password = PasswordField('Пароль', [validators.InputRequired(), validators.Length(min=6, max=100)]) # Password field
    name = StringField('Имя пользователя', [validators.Length(min=4, max=50)]) # Name field
    age = IntegerField('Возраст', [validators.InputRequired(), validators.Length(min=1, max=3)]) # Age field
    submit = SubmitField('Зарегистрироваться') # Submit

class EditUserForm(FlaskForm):
    password = PasswordField('Пароль', [validators.InputRequired(), validators.Length(min=6, max=100)]) # Password field
    name = StringField('Имя пользователя', [validators.Length(min=4, max=50)]) # Name field
    age = IntegerField('Возраст', [validators.InputRequired(), validators.Length(min=1, max=3)]) # Age field
    submit = SubmitField('Сохранить')

