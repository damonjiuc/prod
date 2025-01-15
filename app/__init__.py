from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.extensions import db, login_manager, mail
from app.config import Config

from app.routes.main import main
from app.routes.admin import admin
from app.routes.user import user

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 60}


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