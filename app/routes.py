from flask import render_template, request, redirect, url_for, flash
from app import app, db, bcrypt
from app.models import User
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user, login_required


# Главная страница (доступна только для авторизованных пользователей)
@app.route('/')
@login_required
def index():
    return render_template('index.html')


# Функция регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Проверка уникальности имени пользователя
        if User.query.filter_by(username=form.username.data).first():
            flash('Имя пользователя уже занято. Пожалуйста, выберите другое.', 'danger')
            return redirect(url_for('register'))

        # Хэширование пароля и сохранение пользователя
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


# Функция входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверно введены данные аккаунта. Проверьте имя пользователя и пароль.', 'danger')
    return render_template("login.html", form=form)


# Функция выхода из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('login'))


# Функция увеличения количества кликов
@app.route('/click')
@login_required
def click():
    current_user.clicks += 1
    db.session.commit()
    flash('Клик добавлен!', 'success')
    return redirect(url_for('index'))
