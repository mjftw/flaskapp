from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Regexp
from flask_login import current_user
from webapp.models import User


class SetUsernameMixin():
    new_username = StringField('Username', validators=[
        DataRequired(), Length(min=4, max=32), Regexp(
        '^[a-zA-Z0-9_]+$', message="Username must not contain any special characters except '_'")])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("This username is taken. Please try another".format(
                username))

class SetEmailMixin():
    new_email = StringField('Email', validators=[DataRequired(), Email()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("An account already exists with this email address")


class SetPasswordMixin():
    new_password = PasswordField('Password', validators=[
        DataRequired(), Length(min=8, max=128)])
    new_password2 = PasswordField('Repeat Password', validators=[
        DataRequired(), EqualTo('new_password')])


class CheckUserPasswordMixin():
    password = PasswordField('Current Password', validators=[DataRequired()])

    def validate_password(self, password):
        if current_user.is_anonymous:
            raise ValidationError("User must be signed in")
        if not current_user.password_check(password.data):
            raise ValidationError("Incorrect password")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm, SetEmailMixin, SetUsernameMixin, SetPasswordMixin):
    submit = SubmitField('Register')


class ChangeUserEmailForm(FlaskForm, SetEmailMixin, CheckUserPasswordMixin):
    submit = SubmitField('Confirm')


class ChangeUserUsernameForm(FlaskForm, SetUsernameMixin, CheckUserPasswordMixin):
    submit = SubmitField('Confirm')

class ChangeUserPasswordForm(FlaskForm, SetPasswordMixin, CheckUserPasswordMixin):
    submit = SubmitField('Confirm')

class DeleteUserForm(FlaskForm, CheckUserPasswordMixin):
    submit = SubmitField('Delete Account')
