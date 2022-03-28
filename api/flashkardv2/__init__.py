import csv
import imp
import time
from celery import current_app
from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from os import path
from functools import wraps
import jwt
from flask_mail import Mail
from celery import Celery
from flask_cors import CORS
from flask_caching import Cache
from celery.schedules import crontab, timedelta
from pytz import timezone

# from flask_apscheduler import APScheduler












db = SQLAlchemy()
mail = Mail()
cache = Cache(config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_URL':'redis://localhost:6379/0',
    'CACHE_KEY_PREFIX': 'flashkardv2'
    })
celery = Celery(
    __name__,
    backend='redis://localhost:6379/0',
    broker='redis://localhost:6379/0',
    # include=['flashkardv2.views'],
    imports = ('flashkardv2.views'),
    
)


# scheduler = APScheduler()
DB_NAME = "project.sqlite3"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abulaman'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_DEBUG'] = True
    app.config['MAIL_USERNAME'] = 'tinystarkfordjango@gmail.com'
    app.config['MAIL_PASSWORD'] = 'djangoemail8'
    app.config['MAIL_DEFAULT_SENDER'] = 'tinystarkfordjango@gmail.com'
    app.config['MAIL_MAX_EMAILS'] = None
    # app.config['MAIL_SUPPRESS_SEND'] = False
    app.config['MAIL_ASCII_ATTACHMENTS'] = False
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config['CELERYBEAT_SCHEDULE'] = {
    # Executes every minute
    'periodic_task-every-minute': {
        'task': 'flashkardv2.views.reminder',
        'schedule':crontab(minute=9, hour='*')
    }
}

    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    CORS(app)
    # celery.__init__(
    #     app.import_name, 
    #     backend=app.config['CELERY_RESULT_BACKEND'],
    #     broker=app.config['CELERY_BROKER_URL'],
    #     CELERY_IMPORTS = ("flashkardv2.views", )
    #     )
    celery.conf.update(app.config)
    
    
    # scheduler.init_app(app)
    # scheduler.start()


    from .views import views

    app.register_blueprint(views, url_prefix="/")

    from .models import User, Deck, Card

    create_db(app)

    


    return  app

def create_db(app):
    if not path.exists("flashkard/"+ DB_NAME):
        db.create_all(app=app)
    print('DATABASE ALREADY EXISTS')

def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid/Missing token'}), 401
    return decorated


# def make_celery(app):
#     celery = Celery(
#         app.name,
#         backend=app.config['CELERY_RESULT_BACKEND'],
#         broker=app.config['CELERY_BROKER_URL']
#     )
#     celery.conf.update(app.config)

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery
