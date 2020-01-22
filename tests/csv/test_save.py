"""
Tests for csv/save endpoint
"""
# pylint: disable=unused-import
import json

from flask import current_app, url_for

from pa import db
from pa.fin.models import Account, Record
from pa.fin.routes.csv.save import FILES_NOT_FOUND_ERROR_MESSAGE, INVALID_FILES_ERROR_MESSAGE

from tests.test_fin import client, generate_filename


# pylint: enable=unused-import

# pylint: disable=redefined-outer-name
def test_csv_save(client):
    """
    Test csv/save endpoint with next cases:
        Incorrect request
        Empty request
        Invalid request
        Valid request
        Duplicate request
    """
    # Incorrect request
    with current_app.test_request_context():
        response = client.get(url_for('csv.save'))
        assert response.status_code == 405
    # Empty request
    with current_app.test_request_context():
        response = client.post(url_for('csv.save'))
        assert response.status_code == 400
        assert FILES_NOT_FOUND_ERROR_MESSAGE == \
               json.loads(response.data.decode('utf-8').strip()).get('error')
    # Invalid request
    invalid_files = {
        'data': '\"{\"UAH_p2p.csv\":['
                '{\"date\":\"2019-09-13T21:00:00.000Z\",'
                '\"amount\":\"686,67\",'
                '\"category\":false}]}\"'
    }
    with current_app.test_request_context():
        response = client.post(url_for('csv.save'),
                               content_type='multipart/form-data',
                               data=invalid_files)
        assert response.status_code == 400
        assert INVALID_FILES_ERROR_MESSAGE == \
               json.loads(response.data.decode('utf-8').strip()).get('error')
    # Valid request
    valid_files = {
        'data': '{\"UAH_p2p.csv\":['
                '{\"date\":\"2019-09-13T21:00:00.000Z\",'
                '\"amount\":\"686,67\",'
                '\"category\":false}]}'
    }
    with current_app.test_request_context():
        response = client.post(url_for('csv.save'),
                               content_type='multipart/form-data',
                               data=valid_files)
        assert response.status_code == 200
    # Duplicate request
    valid_files = {
        'data': '{\"UAH_p2p.csv\":['
                '{\"date\":\"2019-09-13T21:00:00.000Z\",'
                '\"amount\":\"686,67\",'
                '\"category\":false}]}'
    }
    with current_app.test_request_context():
        response = client.post(url_for('csv.save'),
                               content_type='multipart/form-data',
                               data=valid_files)
        # pylint: disable=no-member
        assert db.session.query(Account).count() == 1
        assert db.session.query(Record).count() == 1
