import os

class Config():
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or "ep2gz+zx)edg2LM{"