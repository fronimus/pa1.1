"""
    Set of helpful methods for tests
"""
import random
import string

import pytest

from fin import create_app


@pytest.fixture
def client():
    """
    Flask client fixture
    """
    app = create_app()

    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()
    with app.app_context():
        yield testing_client

    ctx.pop()


def generate_filename(length=10):
    """
    Function that generates random string
    """
    chars = string.digits + string.ascii_letters + string.punctuation
    return ''.join(random.choices(chars, k=length))
