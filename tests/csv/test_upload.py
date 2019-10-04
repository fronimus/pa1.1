"""
Test for csv/upload endpoint
"""
from io import BytesIO

from flask import current_app, url_for

from pa.fin.routes.csv.upload import PROCESSING_ERROR_MESSAGE, FILES_NOT_FOUND_ERROR_MESSAGE
# pylint: disable=unused-import
from tests.test_fin import client, generate_filename
# pylint: enable=unused-import

# pylint: disable=redefined-outer-name
def test_csv_upload(client):
    """
    In this test we sending on endpoint wrong and valid files
    """
    invalid_files_names = [generate_filename(), generate_filename()]
    invalid_files = {
        'files[]': [(BytesIO(b'test_file1'), invalid_files_names[0]),
                    (BytesIO(b'test_file2'), invalid_files_names[1])],
    }
    with current_app.test_request_context():
        response = client.post(url_for('csv.upload'),
                               content_type='multipart/form-data',
                               data=invalid_files,
                               follow_redirects=True)
        data = response.data.decode('utf-8')
        assert PROCESSING_ERROR_MESSAGE.format(invalid_files_names[0]) in data
        assert PROCESSING_ERROR_MESSAGE.format(invalid_files_names[1]) in data

    with current_app.test_request_context():
        response = client.post(url_for('csv.upload'), content_type='multipart/form-data', data={},
                               follow_redirects=True)
        data = response.data.decode('utf-8')
        assert FILES_NOT_FOUND_ERROR_MESSAGE in data

    valid_files_names = [generate_filename(), generate_filename()]
    valid_files = {
        'files[]': [(BytesIO(b'date;amount;category'), valid_files_names[0]),
                    (BytesIO(b'date;amount;category'), valid_files_names[1])],
    }
    with current_app.test_request_context():
        response = client.post(url_for('csv.upload'),
                               content_type='multipart/form-data',
                               data=valid_files,
                               follow_redirects=True)
        data = response.data.decode('utf-8')

        assert PROCESSING_ERROR_MESSAGE.format(valid_files_names[0]) not in data
        assert PROCESSING_ERROR_MESSAGE.format(valid_files_names[1]) not in data
        assert valid_files_names[0] in data
        assert valid_files_names[1] in data
