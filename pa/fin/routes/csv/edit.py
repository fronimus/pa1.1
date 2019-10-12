"""
Module for csv edit endpoint
"""
from flask import render_template

from pa.fin.routes.csv import csv


@csv.route('/csv/edit')
def edit():
    """
    Endpoint that responsive to edit csv file
    """
    return 'Nothing here'
