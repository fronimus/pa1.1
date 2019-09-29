"""
Module for csv edit endpoint
"""
from flask import render_template

from fin.routes.csv import csv


@csv.route('/csv/edit')
def edit(dfs=None):
    """
    Endpoint that responsive to edit csv file
    """
    return render_template('csv/edit.jinja2', dfs=dfs)
