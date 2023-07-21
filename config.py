import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	# Задается секретный ключ либо переменной среды, либо по умолчанию.
	default_secret_key = 'fe4!32@fsfd(ff^d$^%px41*&xpef$%gfexpg^%hf42435'
	SECRET_KEY = os.environ.get('SECRET_KEY') or default_secret_key

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'fexp.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False