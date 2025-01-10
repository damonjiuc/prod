from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .extensions import db, login_manager, mail
from .config import Config

from .routes.main import main
from .routes.admin import admin
from .routes.user import user


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 280}


    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(user)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # LOGIN MANAGER
    login_manager.login_view = 'user.user_login'
    login_manager.login_message = 'У Вас нету доступа к данной странице, сначала авторизуйтесь!'


    with app.app_context():
        db.create_all()


    return app