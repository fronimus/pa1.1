# pylint: disable-all
"""
Creating Flask app
"""
import logging

from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler()


def create_app(config_class=Config):
    """
    Functional that creating Flask app from config
    """
    logging.basicConfig(filename='logs/' + __name__ + '.log', level=logging.ERROR)
    app = Flask(__name__)
    app.config.from_object(config_class)

    scheduler.init_app(app)
    scheduler.start()
    db.init_app(app)
    migrate.init_app(app, db)

    from .fin.routes.csv import csv
    from .fin.routes.asset import asset
    from .site import site

    app.register_blueprint(asset, url_prefix='/fin')
    app.register_blueprint(csv, url_prefix='/fin')
    app.register_blueprint(site)
    app.jinja_env.filters['zip'] = zip
    return app
