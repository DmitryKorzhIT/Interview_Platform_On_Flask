import os

basedir = os.path.abspath(os.path.dirname(__file__))
# __file__ представляет файл, из которого выполняется код
# os.path.dirname(__file__) дает вам каталог, в котором находится файл
# os.path.abspath(path) - возвращает нормализованный абсолютный путь


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1@localhost/Interview_Platform'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1'
    DEBUG = True
