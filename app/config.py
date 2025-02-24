import os


class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = '/static/upload/'
    UPLOAD_PATH_FULL = ROOT + UPLOAD_PATH


# DB
    USER = os.environ.get('MYSQL_USER')
    PASSWORD = os.environ.get('MYSQL_PASSWORD')
    HOST = os.environ.get('MYSQL_HOST')
    PORT = os.environ.get('MYSQL_PORT')
    DB = os.environ.get('MYSQL_DB')

    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# end DB

# mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# end mail

# firebase
    FIREBASE_CREDENTIALS = os.path.join(ROOT, 'firebase_credentials.json')
# end firebase

    JSONIFY_PRETTYPRINT_REGULAR = False