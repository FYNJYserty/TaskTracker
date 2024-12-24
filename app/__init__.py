from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
# Подключение Bootstrap5
bootstrap = Bootstrap5(app)
# Инициализация менеджера логина
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# Импорт маршрутов
from app import routes
