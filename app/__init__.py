# -*- coding: utf-8 -*-
'''
Created on 2017年3月3日

@author: guxiwen
'''

from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'
def create_app():
    app = Flask(__name__)

    from .main import main as main__blueprint
    from app.user import user as user__blueprint
    app.config['SECRET_KEY'] = 'hehe'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#     app.config.from_object(Config())
    app.register_blueprint(main__blueprint)
    app.register_blueprint(user__blueprint,url_prefix='/user')
    db.init_app(app)
#     scheduler.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
#     scheduler.start()
    return app


