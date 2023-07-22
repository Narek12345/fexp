from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from fexp import db
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    
    username = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registration_time = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(10))

    def __repr__(self):
        return f'{self.id}:{self.username}'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    

class Employer(db.Model):
    __tablename__ = 'employer'
    id = db.Column(db.Integer(), primary_key=True)
    
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'{self.id}:{self.first_name}'


class Student(db.Model):
    tablename = 'student'
    id = db.Column(db.Integer(), primary_key=True)

    first_name = db.Column(db.String())
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    user = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def repr(self):
        return f'{self.id}:{self.first_name}'


class JobVacansy(db.Model):
    __tablename__ = 'job_vacansy'
    id = db.Column(db.Integer(), primary_key=True)

    title = db.Column(db.String(255))
    salary = db.Column(db.Integer())
    description = db.Column(db.String(255))
    experience = db.Column(db.String(255))
    company = db.Column(db.String(255))
    country = db.Column(db.String(255))
    city = db.Column(db.String(255))
    adress = db.Column(db.String(255))

    employer = db.Column(db.Integer, db.ForeignKey('employer.id'))
    
    def __repr__(self):
        return f'{self.id}:{self.title}'


class Summary(db.Model):
    tablename = 'summary'
    id = db.Column(db.Integer(), primary_key=True)

    title = db.Column(db.String(255))
    salary = db.Column(db.Integer(), default=None)
    age = db.Column(db.Integer(), default=None)
    experience = db.Column(db.String(255))
    country = db.Column(db.String(255))
    city = db.Column(db.String(255))
    adress = db.Column(db.String(255))
    skills = db.Column(db.String(150))
    biography = db.Column(db.String(1000))
    
    student = db.Column(db.Integer(), db.ForeignKey('student.id'))

    def repr(self):
        return f'{self.id} {self.title}'