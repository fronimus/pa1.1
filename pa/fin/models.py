# pylint: disable=no-member
"""
Module for PA models
"""
from pa import db


# pylint: disable=too-few-public-methods
class Record(db.Model):
    """
    The model that represents an entry in an accounting journal
    """
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    is_replenish = db.Column(db.Boolean, nullable=False, default=True)
# pylint: enable=too-few-public-methods
