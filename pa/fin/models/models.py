# pylint: disable=no-member
"""
Module for PA models
"""
from sqlalchemy.orm import relationship

from pa import db

# pylint: disable=too-few-public-methods
from pa.fin.models.enum import Currency


class Record(db.Model):
    """
    The model that represents an entry in an accounting journal
    """
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    asset = relationship('Asset', back_populates='records')
    date = db.Column(db.Date, nullable=False, index=True)
    amount = db.Column(db.Numeric(precision=10, scale=2, asdecimal=True), nullable=False)
    is_replenish = db.Column(db.Boolean, nullable=False, default=True)


class Asset(db.Model):
    """
    The model that represents an asset
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=25), nullable=False, index=True)
    currency = db.Column(db.Enum(Currency), nullable=False, index=True)
    records = relationship('Record', back_populates='asset')


class Inflation(db.Model):
    """
    The model that represents an inflation
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    rate = db.Column(db.Numeric(precision=10, scale=2, asdecimal=True), nullable=False)
