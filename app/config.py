import os


class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = '/static/upload/'
    UPLOAD_PATH_FULL = ROOT + UPLOAD_PATH


# DB
    USER = os.environ.get('MYSQL_USER', 'quicksteps_tests')
    PASSWORD = os.environ.get('MYSQL_PASSWORD', 'tests')
    HOST = os.environ.get('MYSQL_HOST', 'vh436.timeweb.ru')
    PORT = os.environ.get('MYSQL_PORT', '3306')
    DB = os.environ.get('MYSQL_DB', 'quicksteps_tests')

    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hklfkjtgoidfv3456546nfdg5645df6456zfsj')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
# end DB

# mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.mail.ru')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', False)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'no-reply@prod.ru')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'r7aWEXfN4B5WwFkb4Du4')
    ADMINS = ['damonjiuc@gmail.com']
# end mail