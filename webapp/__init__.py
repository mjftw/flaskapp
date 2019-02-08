from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_bootstrap import Bootstrap
import ssl
import os.path

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

project_root = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))

# SSL cert & key should be symlinked to project root dir
ssl_crt = os.path.join(project_root, 'cert.pem')
ssl_key = os.path.join(project_root, 'privkey.pem')
ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_ctx.load_cert_chain(certfile=ssl_crt, keyfile=ssl_key)