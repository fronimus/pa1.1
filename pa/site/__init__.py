"""
Blueprint for site
"""
from flask import Blueprint
# pylint: disable=invalid-name
site = Blueprint('site', __name__, template_folder='templates',)
# pylint: enable=invalid-name
# pylint: disable=wrong-import-position
from .routes.dashboard import *
# pylint: enable=wrong-import-position
