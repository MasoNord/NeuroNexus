from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка строки подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Для SQLite
# Для MySQL:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://user:password@localhost/db_name'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключить предупреждения

db = SQLAlchemy(app)

# Определите модели
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Создайте все таблицы
with app.app_context():
    db.create_all()

from registration_form import routes
