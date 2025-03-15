from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    first_name = StringField(label='Имя пользователя', validators=[DataRequired(), Length(min = 3, max=50)])
    second_name = StringField(label='Фамилия пользователя', validators=[DataRequired(), Length(min = 3, max=150)])
    login = StringField(label='Логин', validators=[DataRequired(), Length(min = 5, max = 50)])
    email = StringField(label='Электронная почта', validators=[DataRequired(), Length(min = 5, max = 100)])
    password = PasswordField(label='Пароль', validators=[DataRequired(), Length(min = 8, max = 30)])
    confirm_password = PasswordField(label='Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Sign Up')

class LoginForm(FlaskForm):
    email = StringField(label='Электронная почта', validators=[DataRequired(), Length(min = 5, max = 100)])
    password = PasswordField(label='Пароль', validators=[DataRequired(), Length(min = 8, max = 30)])
    submit = SubmitField(label='Login')
