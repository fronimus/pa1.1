from flask import render_template, current_app

from pa import db
from pa.fin.models import Account
from pa.fin.routes.account import account_blueprint


@account_blueprint.route('account/list')
def account_list():
    current_app.logger.info(db.session.query(Account).count())
    return render_template('account/list.jinja2', account_query=db.session.query(Account))
