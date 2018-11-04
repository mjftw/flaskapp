from random import randint
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from webapp import app
from webapp import db
from webapp.forms import LoginForm, RegisterForm, ChangeUserEmailForm, ChangeUserPasswordForm, DeleteUserForm
from webapp.models import User, UserID


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
        user = User(username=form.new_username.data, email=form.new_email.data)
        user.password_set(form.new_password.data)

        max_id = pow(2, 32)
        user.id = randint(0, max_id)
        while UserID.query.filter_by(user_id=user.id).first():
            user.id = randint(0, max_id)

        db.session.add(UserID(user_id=user.id))
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

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
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