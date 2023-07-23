from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from fexp import app, db
from .models import User


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
    return 'Page login'


@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    return f'Hello {username}'
