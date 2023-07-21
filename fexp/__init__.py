from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Инициализируем Flask.
app = Flask(__name__)

# Указываем местоположение класса с настройками.
app.config.from_object(Config)

# Создаем обьект БД.
db = SQLAlchemy(app)

# Создаем обьект, представляющий собой механизм миграций.
migrate = Migrate(app, db)


from fexp import models, views
