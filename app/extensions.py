from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_ckeditor import CKEditor
from firebase_admin import credentials, initialize_app


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
ckeditor = CKEditor()


def init_firebase():
    # Возвращаем функцию, которая будет инициализировать Firebase Admin SDK
    def init_app(app):
        cred = credentials.Certificate(app.config['FIREBASE_CREDENTIALS'])
        initialize_app(cred)

    return init_app