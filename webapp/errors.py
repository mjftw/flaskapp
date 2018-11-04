from flask import render_template, redirect, url_for

from webapp import app
from webapp import login


@login.unauthorized_handler
def unauthorized():
    return redirect(url_for('noauth'))


@app.route('/noauth')
def noauth():
    return render_template('noauth.html', title='Unauthorised access!')
