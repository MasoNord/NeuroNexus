from registration_form import app, db
from registration_form.forms import RegistrationForm, LoginForm
from registration_form.models import Accounts, db
from flask import render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_by_email = Accounts.query.filter_by(email=form.email.data).first()

        if user_by_email and bcrypt.check_password_hash(user_by_email.password, form.password.data):
            # Здесь перенаправляем на профиль или главную страницу
            return redirect(url_for('index.html'))  # Измените на правильный маршрут
        else:
            flash('Login Unsuccessful. Please check username or password', 'danger')
            return redirect(url_for('profil'))

    # Если неуспешный вход, возвращаем на страницу входа с формой и сообщением
    return render_template('vxod_reg.html', title='Login', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Accounts(
            first_name=form.first_name.data,
            second_name=form.second_name.data,
            login=form.login.data,
            email=form.email.data,
            password=password_hash
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('profil'))
    return render_template('vxod_reg.html', title='Register', form=form)

@app.route('/add_user', methods=['POST'])
def add_user():
    new_user = Accounts(username='example', email='example@example.com')
    db.session.add(new_user)
    db.session.commit()
    return 'User  added!'

@app.route('/profil', methods=['POST', 'GET'])
def profil():
    return render_template('profil.html', title='Profile')


@app.route('/help', methods=['GET'])
def help():
    return render_template('pomosh.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

def list_routes():
    for rule in app.url_map.iter_rules():
        print(rule.endpoint)
