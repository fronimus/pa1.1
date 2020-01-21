from flask import render_template

from pa.fin.routes.dashboard import fin_dashboard_blueprint


@fin_dashboard_blueprint.route('/')
def fin_dashboard():
    return render_template('dashboard/dashboard.jinja2')
