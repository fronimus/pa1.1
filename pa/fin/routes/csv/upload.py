"""
Module for csv upload endpoint
"""
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
    if request.method == "GET":
        return render_template('csv/upload.jinja2')
    if 'files[]' not in request.files:
        flash(FILES_NOT_FOUND_ERROR_MESSAGE)
        return redirect(request.url)
    files = request.files.getlist('files[]')

    dfs = []
    replenish_categories = ['Покупка металов',
                            'Покупка валюты',
                            'replenish',
                            'Покупка криптовалюты']
    for file in files:
        try:
            dataframe = pd.read_csv(file, delimiter=';')
            dataframe.filename = file.filename
            dataframe['category'] = (dataframe['category'].isin(replenish_categories))
            dfs.append(dataframe)
        except KeyError as error:
            current_app.logger.exception(error)
            flash(PROCESSING_ERROR_MESSAGE.format(file.filename))
    return render_template('csv/edit.jinja2', dfs=dfs)
