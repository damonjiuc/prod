import os


class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = '/static/upload/'
    UPLOAD_PATH_FULL = ROOT + UPLOAD_PATH


    USER = os.environ.get('MYSQL_USER', 'quicksteps_tests')
    PASSWORD = os.environ.get('MYSQL_PASSWORD', 'tests')
    HOST = os.environ.get('MYSQL_HOST', 'vh436.timeweb.ru')
    PORT = os.environ.get('MYSQL_PORT', '3306')
    DB = os.environ.get('MYSQL_DB', 'quicksteps_tests')

    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hklfkjtgoidfv3456546nfdg5645df6456zfsj')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
