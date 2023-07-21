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