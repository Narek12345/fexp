from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from fexp import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    
    username = db.Column(db.String(255), index=True, nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), index=True, nullable=True)

    def __repr__(self):
        return f'{self.id}:{self.username}'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    

class Employer(db.Model):
    __tablename__ = 'employer'
    id = db.Column(db.Integer(), primary_key=True)
    
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    company = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255), index=True, nullable=True, unique=True)

    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'{self.id}:{self.first_name}'


class JobVacansy(db.Model):
    __tablename__ = 'job_vacansy'
    id = db.Column(db.Integer(), primary_key=True)

    job_title = db.Column(db.String(255), nullable=True)
    salary = db.Column(db.Integer(), nullable=True)
    description = db.Column(db.String(255))
    experience = db.Column(db.String(255), nullable=True)
    company = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255))
    city = db.Column(db.String(255))
    adress = db.Column(db.String(255))

    userid = db.Column(db.Integer, db.ForeignKey('employer.id'))
    
    def __repr__(self):
        return f'{self.id}:{self.first_name}'

