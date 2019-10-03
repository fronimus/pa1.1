"""
Main dashboard
"""
from flask import render_template

from ...site import site


@site.route('/')
def show():
    return render_template('dashboard.jinja2')
