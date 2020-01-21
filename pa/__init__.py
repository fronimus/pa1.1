# pylint: disable-all
"""
Creating Flask app
"""
import logging

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    """
    Functional that creating Flask app from config
    """
    logging.basicConfig(filename='logs/' + __name__ + '.log', level=logging.ERROR)
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)

    config = app.config
    panels = list(config['DEBUG_TB_PANELS'])
    config['DEBUG_TB_PANELS'] = panels

    from .fin.routes.account import account_blueprint
    from .fin.routes.asset import asset
    from .fin.routes.csv import csv
    from .fin.routes.dashboard import fin_dashboard_blueprint
    from .site import site_blueprint

    app.register_blueprint(account_blueprint, url_prefix='/account')
    app.register_blueprint(asset, url_prefix='/fin')
    app.register_blueprint(csv, url_prefix='/fin')
    app.register_blueprint(fin_dashboard_blueprint, url_prefix='/fin')
    app.register_blueprint(site_blueprint)
    app.jinja_env.filters['zip'] = zip
    return app
