from flask import Flask

from app.extensions import db, login_manager, mail, ckeditor, init_firebase
from app.config import Config

from app.routes.main import main
from app.routes.admin import admin
from app.routes.user import user
from app.routes.firebase import firebase

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 60}


    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(firebase)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    init_firebase()(app)

    # LOGIN MANAGER
    login_manager.login_view = 'user.user_login'
    login_manager.login_message = 'У Вас нету доступа к данной странице, сначала авторизуйтесь!'


    with app.app_context():
        db.create_all()


    return app