"""
Creating Flask app
"""
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .fin.routes.csv import csv
from .site import site
from config import Config

# pylint: disable=invalid-name
db = SQLAlchemy()
migrate = Migrate()


# pylint: enable=invalid-name

def create_app(config_class=Config):
    """
    Functional that creating Flask app from config
    """
    logging.basicConfig(filename='logs/' + __name__ + '.log', level=logging.ERROR)
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(csv, url_prefix='/fin')
    app.register_blueprint(site)
    return app


# pylint: disable=ungrouped-imports
from .fin import models
