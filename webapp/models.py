from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from webapp import db
from webapp import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def password_set(self, password):
        self.password_hash = generate_password_hash(password)

    def password_check(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
