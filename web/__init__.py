from os import getenv
import logging
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def set_loging_level():
    loglevel = getenv('HVZ_LOG_LEVEL', 'ERROR')
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level, 
        format='%(asctime)s %(levelname)s %(module)s %(funcName)s: %(message)s')


def create_app(config_name='default'):
    set_loging_level()

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .main import main
    app.register_blueprint(main)

    from .adminsite import admin
    app.register_blueprint(admin, url_prefix='/admin')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app