from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    load_dotenv()
    SECRET_KEY = os.getenv('SECRET_KEY')
    app.config['SECRET_KEY'] = SECRET_KEY
    print(SECRET_KEY)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
