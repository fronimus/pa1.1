"""
Blueprint for CRUD operations csv files
"""
from flask import Blueprint
# pylint: disable=invalid-name
csv = Blueprint('csv', __name__, template_folder='../../templates/')
# pylint: enable=invalid-name
# pylint: disable=wrong-import-position
from .edit import *
from .upload import *
# pylint: enable=wrong-import-position
