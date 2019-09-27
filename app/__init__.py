from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.routes.cvs.cvs_view import cvs
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(cvs)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
from app.templates import jinja_filters
