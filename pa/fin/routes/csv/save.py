import json
from _decimal import Decimal
from json import JSONDecodeError

import dateutil
from flask import request, jsonify, current_app

from pa import db
from pa.fin.models import Account, Currency, Record
from ..csv import csv

FILES_NOT_FOUND_ERROR_MESSAGE = 'Files Not Found'
INVALID_FILES_ERROR_MESSAGE = 'Invalid File Format'


@csv.route('csv/save', methods=["POST"])
def save():
    raw_data = request.form.get('data')
    if raw_data is None:
        return jsonify({'error': FILES_NOT_FOUND_ERROR_MESSAGE}), 400
    try:
        json_data = json.loads(raw_data)
    except JSONDecodeError as error:
        current_app.logger.exception(error)
        return jsonify({'error': INVALID_FILES_ERROR_MESSAGE}), 400

    account_query = db.session.query(Account.name)
    existing_accounts = [asset.name for asset in account_query]
    new_accounts = [Account(name=name, currency=Currency(name.split('_')[0]))
                  for name in json_data.keys() if name not in existing_accounts]
    if new_accounts:
        db.session.bulk_save_objects(new_accounts)
        db.session.commit()

    involved_accounts = db.session.query(Account).filter(Account.name.in_(json_data.keys()))
    income_records = []
    for account in involved_accounts:
        for record in json_data[account.name]:
            income_records.append(Record(date=dateutil.parser.parse(record['date']).date(),
                                         amount=Decimal(record['amount'].replace(',', '.')),
                                         is_replenish=record['category'],
                                         account_id=account.id))

    record_query = db.session.query(Record)
    new_records = []
    for record in income_records:
        duplicate = False
        for db_record in record_query:
            if record.date == db_record.date \
                    and record.amount == db_record.amount \
                    and record.is_replenish == db_record.is_replenish:
                duplicate = True
                break
        if not duplicate:
            new_records.append(record)
    db.session.bulk_save_objects(new_records)
    db.session.commit()
    return jsonify()
