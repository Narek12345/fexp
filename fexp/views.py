from flask import render_template, request, redirect, url_for

from fexp import app


@app.route('/index')
@app.route('/')
def index():
    return 'Hello world'


@app.route('/list_of_jobs')
def list_of_jobs():
    return render_template('index.html')
