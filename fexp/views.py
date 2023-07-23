from flask import render_template, request, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user

from fexp import app, db, login_manager
from .models import User, Student, Employer


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    user = User()

    if request.method == 'POST':
        # Получаем из формы значения полей и сохраняем их в обьекте User, а затем добавляем этот обьект в БД.
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        if password:
            if not user.query.filter_by(username=username).first():
                try:
                    hash = generate_password_hash(password)            
                    users = User(username=username, password=hash, role=role)

                    db.session.add(users)
                    db.session.commit()

                    flash('Регистрация прошла успешно')
                except:
                    db.session.rollback()
                    flash('error')
            else:
                flash('Имя пользователя уже зарегистрировано')
        else:
            flash('Поле пароля пустое')
    
    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile', username=current_user.username))
            flash('Вы успешно авторизовались ')
    return render_template('login.html')


@login_required
@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)
    
    if user.role == 'student':
        user_info = Student.query.filter_by(user=user.id).first()
    elif user.role == 'employer':
        user_info = Employer.query.filter_by(user=user.id).first()

    return f'Hello {username}'


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user):
    return User.query.get(user)