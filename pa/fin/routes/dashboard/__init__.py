"""
Blueprint for dashboard in fin module
"""
from flask import Blueprint

fin_dashboard_blueprint = Blueprint('fin_dashboard', __name__, template_folder='../../templates/')

from .dashboard import *
