from flask import render_template, request, redirect, url_for, flash

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
        user.username = request.form.get('username')
        password = request.form.get('password')
        user.set_password(password)
        user.role = request.form.get('role')
        db.session.add(user)
        db.session.commit()

        flash('GOOD !', 'info')
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return 'Page login'


@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    return f'Hello {username}'
