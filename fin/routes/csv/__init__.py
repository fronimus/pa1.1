"""
Blueprint for CRUD operations csv files
"""
from flask import Blueprint
# pylint: disable=invalid-name
csv = Blueprint('csv', __name__, template_folder='templates')

from .edit import *
from .upload import *
