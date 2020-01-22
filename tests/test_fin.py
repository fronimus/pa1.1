"""
    Set of helpful methods for tests
"""
import pdb
import random
import string

import pytest

from config import TestConfig
from pa import create_app, db


@pytest.fixture
def client():
    """
    Flask client fixture
    """
    app = create_app(TestConfig)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    ctx = app.app_context()
    ctx.push()
    with app.app_context():
        yield app.test_client()

    with app.app_context():
        db.drop_all()
    ctx.pop()

def generate_filename(length=10):
    """
    Function that generates random string
    """
    chars = string.digits + string.ascii_letters
    return ''.join(random.choices(chars, k=length))
