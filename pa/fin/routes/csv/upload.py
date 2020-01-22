"""
Module for csv upload endpoint
"""
import json
import pdb

import pandas as pd
from flask import render_template, request, flash, redirect, current_app

from pa.fin.routes.csv import csv

PROCESSING_ERROR_MESSAGE = 'Error while processing {} file'
FILES_NOT_FOUND_ERROR_MESSAGE = 'No file part'


@csv.route('/csv/upload', methods=['GET', 'POST'])
def upload():
    """
    Endpoint that responsive to uploading csv files
    """
    # pdb.set_trace()
    if request.method == "GET":
        return render_template('csv/upload.jinja2')
    if 'files[]' not in request.files:
        flash(FILES_NOT_FOUND_ERROR_MESSAGE)
        return redirect(request.url)
    files = request.files.getlist('files[]')

    data = []
    replenish_categories = ['Покупка металов',
                            'Покупка валюты',
                            'replenish',
                            'Покупка криптовалюты']
    for file in files:
        try:
            dataframe = pd.read_csv(file, delimiter=';', usecols=['date', 'amount', 'category'])
            dataframe['category'] = (dataframe['category'].isin(replenish_categories))
            data.append(json.dumps({file.filename: dataframe.to_json()}))

        except (ValueError, KeyError) as error:
            current_app.logger.exception(error)
            flash(PROCESSING_ERROR_MESSAGE.format(file.filename))
    return render_template('csv/edit.jinja2', data=data)
