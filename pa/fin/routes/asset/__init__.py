"""
Blueprint for CRUD operation on asset
"""
from flask import Blueprint

asset = Blueprint('asset', __name__, template_folder='../../templates/')

from .list import *
