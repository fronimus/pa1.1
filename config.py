"""
Module for Flask app configs
"""
import os


# pylint: disable=too-few-public-methods
class Config:
    """
    Standard Flask config
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
# pylint: enable=too-few-public-methods
