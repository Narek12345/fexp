from flask import render_template, request, redirect, url_for

from fexp import app


@app.route('/index')
@app.route('/')
def index():
    return 'Hello world'
