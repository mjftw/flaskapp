from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user

from webapp import app
from webapp.forms import LoginForm
from webapp.models import User

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Merlin'}
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.password_check(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        if login_user(user, remember=form.remember_me.data):
            flash('Log in successful')
        else:
            flash('Unable to log in user')
            return redirect(url_for('login'))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out')
    return redirect(url_for('index'))
