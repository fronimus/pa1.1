"""
Blueprint for site
"""
from flask import Blueprint

site = Blueprint('site', __name__, template_folder='templates',)

from .routes.dashboard import *
