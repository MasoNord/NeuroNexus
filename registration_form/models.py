from registration_form import db
import mysql.connector
import bcrypt

class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    second_name = db.Column(db.String(150), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, first_name, second_name, login, email, password):
        self.first_name = first_name
        self.second_name = second_name
        self.login = login
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User({self.username}, {self.email})"
