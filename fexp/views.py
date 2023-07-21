from flask import render_template

from fexp import app, models


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    return 'Page register'


@app.route('/login', methods=['POST', 'GET'])
def login():
    return 'Page login'


@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    return f'Hello {username}'
