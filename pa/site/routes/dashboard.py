"""
Main dashboard
"""
from flask import render_template

from ...site import site_blueprint


@site_blueprint.route('/')
def dashboard():
    return render_template('dashboard.jinja2')
