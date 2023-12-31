from flask import render_template, request, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.exc import IntegrityError

from fexp import app, db
from .auth import load_user
from .email import send_email_msg
from .models import User, Student, Employer, JobVacansy, Summary
from .forms import EmployerForm, StudentForm, JobVacansyForm, SummaryForm


@app.route('/index')
@app.route('/')
def index():
    # Проверяем, зарегестрирован пользователь или нет.
    if current_user.is_authenticated:

        # Проверяем, кем является пользователь: student/employer.
        if current_user.role == 'student':
            # Составляем запрос для вывода всех последних 10 вакансий.
            latest_10_vacancies = JobVacansy.query.all()[:10]
            return render_template('index.html', latest_10_vacancies=latest_10_vacancies)

        elif current_user.role == 'employer':
            # Составляем запрос для вывода всех полследних 10 резюме.
            latest_10_summary = Summary.query.all()[:10]
            return render_template('index.html', latest_10_summary=latest_10_summary)

    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        # Получаем из формы значения полей и сохраняем их в обьекте User, а затем добавляем этот обьект в БД.
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        if password:
            if not User.query.filter_by(username=username).first():
                try:
                    hash = generate_password_hash(password)            
                    users = User(username=username, password=hash, role=role)

                    db.session.add(users)
                    db.session.commit()

                    flash('Регистрация прошла успешно')
                    return redirect(url_for('login'))
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

        if username and password:
            user = User.query.filter_by(username=username).first()
        
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('profile', username=current_user.username))
    return render_template('login.html')


@login_required
@app.route('/profile/<username>', methods=['POST', 'GET'])
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)

    if user.role == 'student':
        # Получаем информацию о текущем пользователе.
        user_info = Student.query.filter_by(user=user.id).first()
        # Получаем все резюме текущего пользователя.
        summary = Summary.query.filter_by(student=user_info.id).all()
        # Создаем пустую форму для создания своего профиля.
        form = StudentForm()

        # Проверяем, что пользователь зарегестрировал свой профиль. В противном случае отправляем форму для ввода.
        if user_info:
            profile_info = Student.query.filter_by(user=user.id).first()

            # Отрисовываем страницу для зарегестрированного пользователя
            return render_template('profile.html', profile_info=profile_info, user=user, summary=summary, registered_profile=True)
        else:
            form = StudentForm(request.form)

            # Проверка формы на валидность.
            if form.validate_on_submit():

                # Создаем профиль студента.
                new_student = Student(first_name=form.data['first_name'], last_name=form.data['last_name'], phone_number=str(form.data['phone_number']), email=form.data['email'], user=user.id)

                # Сохраняем его в БД и перенаправляем пользователя на его страницу с уже сохраненным профилем.
                db.session.add(new_student)
                db.session.commit()
                return redirect(url_for('profile', username=username))

    elif user.role == 'employer':
        # Получаем информацию о текущем пользователе.
        user_info = Employer.query.filter_by(user=user.id).first()
        # Получаем все вакансий текущего пользователя.
        vacansy = JobVacansy.query.filter_by(employer=user_info.id).all()
        # Создаем пустую форму для создания своего профиля.
        form = EmployerForm()

        # Проверяем, что пользователь зарегестрировал свой профиль. В противном случае отправляем форму для ввода.
        if user_info:
            profile_info = Employer.query.filter_by(user=user.id).first()
            
            # Отрисовываем страницу для зарегестрированного пользователя
            return render_template('profile.html', profile_info=profile_info, user=user, vacansy=vacansy, registered_profile=True)
        else:
            form = EmployerForm(request.form)

            # Проверка формы на валидность.
            if form.validate_on_submit():
                
                # Создаем профиль работодателя.
                new_employer = Employer(first_name=form.data['first_name'], last_name=form.data['last_name'], phone_number=str(form.data['phone_number']), email=form.data['email'], user=user.id)            
                try:
                    # Сохраняем его в БД и перенаправляем пользователя на его страницу с уже сохраненным профилем.
                    db.session.add(new_employer)
                    db.session.commit()
                    return redirect(url_for('profile', username=username))
                except IntegrityError:
                    db.session.rollback()
                    flash('Такой email уже есть !')

    # Отрисовываем страницу не для зарегестрированного пользователя.
    return render_template('profile.html', form=form, username=username, registered_profile=False, user=user)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
@app.route('/create_job_vacansy', methods=['POST', 'GET'])
def create_job_vacansy():
    form = JobVacansyForm(request.form)

    if form.validate_on_submit():
        # Получить id текущего пользователя.
        current_user_id = current_user.id
        # Делаем запрос к Employer чтобы взять его id для модели JobVacansy.
        employer_id = Employer.query.filter_by(user=current_user_id).first().id

        new_job_vacansy = JobVacansy(title=form.data['title'], salary=form.data['salary'], description=form.data['description'], experience=form.data['experience'], company=form.data['company'], country=form.data['country'], city=form.data['city'], necessary_skills=form.data['necessary_skills'], employer=employer_id)

        db.session.add(new_job_vacansy)
        db.session.commit()
        return redirect(url_for('profile', username=current_user.username))
    
    return render_template('create_job_vacansy.html', form=form)


@login_required
@app.route('/create_summary', methods=['POST', 'GET'])
def create_summary():
    form = SummaryForm(request.form)

    if form.validate_on_submit():
        # Получаем id текущего пользователя.
        current_user_id = current_user.id
        # Делаем запрос к Student чтобы взять его id для модели Summary.
        student_id = Student.query.filter_by(user=current_user_id).first().id
        
        new_summary = Summary(title=form.data['title'], salary=form.data['salary'], age=form.data['age'], experience=form.data['experience'], country=form.data['country'], city=form.data['city'], skills=form.data['skills'], biography=form.data['biography'], student=student_id)

        db.session.add(new_summary)
        db.session.commit()
        return redirect(url_for('profile', username=current_user.username))

    return render_template('create_summary.html', form=form)