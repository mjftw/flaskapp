from flask import render_template, redirect, url_for

from webapp import app, login, db


@login.unauthorized_handler
def unauthorized():
    return redirect(url_for('noauth'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html', title='Page not found'), 404

@app.errorhandler(500)
def not_found_error(error):
    db.session.rollback()
    return render_template('errors/500.html', title='Unexpected error'), 500
