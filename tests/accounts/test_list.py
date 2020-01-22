import pdb

from flask import current_app, url_for

from pa import db
from pa.fin.models import Account, Currency

from tests.test_fin import client


def test_account_list(client):
    test_names = ['TestAccount1', 'TestAccount2']
    db.session.bulk_save_objects([Account(name=test_names[0], currency=Currency.USD),
                                  Account(name=test_names[1], currency=Currency.UAH)])
    db.session.commit()
    with current_app.test_request_context():
        response = client.get(url_for('account.account_list'))
        for name in test_names:
            assert name in response.data.decode('utf-8')
