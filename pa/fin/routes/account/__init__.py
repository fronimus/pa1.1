"""
Blueprint for CRUD operation on account
"""
from flask import Blueprint

account_blueprint = Blueprint('account', __name__, template_folder='../../templates/')

from .action import *
