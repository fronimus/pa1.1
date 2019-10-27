"""
    Set of helpful methods for tests
"""
import random
import string

import pytest

from pa import create_app, db


@pytest.fixture
def client():
    """
    Flask client fixture
    """
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.config['DEBUG'] = True
    app.config['TESTING'] = True

    ctx = app.app_context()
    ctx.push()
    with app.app_context():
        yield app.test_client()

    ctx.pop()


def generate_filename(length=10):
    """
    Function that generates random string
    """
    chars = string.digits + string.ascii_letters
    return ''.join(random.choices(chars, k=length))
