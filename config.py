import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Задается секретный ключ либо переменной среды, либо по умолчанию.
    default_secret_key = 'fe4!32@fsfd(ff^d$^%px41*&xpef$%gfexpg^%hf42435'
    SECRET_KEY = os.environ.get('SECRET_KEY') or default_secret_key

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'fexp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
  
    # Настройки для flask-mail.
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'fexpcompany@gmail.com'
    MAIL_DEFAULT_SENDER = 'fexpcompany@gmail.com'
    MAIL_PASSWORD = 'lfzhrvaagoeqmdez'


class UserLogin():
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.__user['id'])
