import json
import requests
from random import randint
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from webapp import app
from webapp import db
from webapp.forms import LoginForm, RegisterForm, ChangeUserEmailForm, ChangeUserPasswordForm, DeleteUserForm
from webapp.models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.new_username.data,
            email=form.new_email.data,
            is_admin=False)
        user.password_set(form.new_password.data)

        db.session.add(user)
        db.session.commit()

        logout_user()
        login_user(user)
        flash("New user {} created!".format(user.username))
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

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

@app.route('/user/', methods=['GET', 'POST'])
@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username=''):
    user = User.query.filter_by(username=username).first_or_404()
    edit = request.args.get('edit')

    form = None
    if current_user.username == user.username:
        if edit == "email":
            form = ChangeUserEmailForm()
            if form.validate_on_submit():
                user.email = form.new_email.data
                db.session.add(user)
                db.session.commit()
                flash("Email address changed")
                return redirect(url_for('user', username=username))

        elif edit == "password":
            form = ChangeUserPasswordForm()
            if form.validate_on_submit():
                user.password_set(form.new_password.data)
                db.session.add(user)
                db.session.commit()
                flash("Password changed")
                return redirect(url_for('user', username=username))

        elif edit == "delete":
            form = DeleteUserForm()
            if form.validate_on_submit():
                logout_user()
                db.session.delete(user)
                db.session.commit()
                flash("Account deleted")
                return redirect(url_for('index'))

    return render_template(
        'user.html', title='Account', user=user, edit=edit, form=form)

@app.route('/brewcontrol')
@login_required
def brewcontrol():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    node_urls = [
        'http://192.168.0.35:5010',
        'http://192.168.0.35:5020',
        'http://192.168.0.35:5030'
    ]
    api_nodes = []
    for u in node_urls:
        r = requests.get(u)
        t = r.text
        if t:
            api_nodes.append(json.loads(r.text))
    return render_template('brewcontrol.html', title='Brewing Control Panel', nodes=api_nodes)

#TODO: Impliment a way of making API calls from within brewing control panel
# @app.context_processor
# def utility_processor():
#     def call_api_node(host, port, method):
#         if host and port and method:
#             url = "http://{}:{}/{}".format(host, port, method)
#             r = requests.post(url)
#             print('Made API call: {}. Method returned: {}'.format(url, r.text))
#             return(r.text)

# Dummy route is here so that we can link to the flask-admin page
@app.route('/admin')
def admin():
    flash('Admin panel unavailable')
    return redirect(url_for('index'))

@app.route('/noauth')
def noauth():
    return render_template('errors/noauth.html', title='Unauthorised access!')
