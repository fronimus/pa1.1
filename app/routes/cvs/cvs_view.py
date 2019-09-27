import pandas
from flask import Blueprint, render_template, request, flash, redirect

cvs = Blueprint('cvs', __name__, template_folder='templates')


@cvs.route('/cvs/view', methods=['GET', 'POST'])
def view():
    if request.method == 'GET':
        return render_template('cvs_view.jinja2')
    elif request.method == "POST":
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')

        dfs = []
        for file in files:
            cvs = pandas.read_csv(file, delimiter=';')
            cvs._filename = file.filename
            dfs.append(cvs)
        return render_template('cvs_detailed_view.jinja2', dfs=dfs)
