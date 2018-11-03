import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = (os.environ.get('FLASK_SECRET_KEY')
        or "ep2gz+zx)edg2LM{")
    SQLALCHEMY_DATABASE_URI = (os.environ.get('FLASK_DATABASE_URL')
        or 'sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
