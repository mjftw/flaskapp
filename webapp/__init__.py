from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_bootstrap import Bootstrap

from .config import Config

app = Flask(__name__)
app.config.from_object(Config())
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
bootstrap = Bootstrap(app)

from webapp import routes, errors, models
from webapp.admin_views import UserIsAdminIndexView, UserIsAdminModelView

admin = Admin(app, index_view=UserIsAdminIndexView())
admin.add_view(UserIsAdminModelView(models.User, db.session))
