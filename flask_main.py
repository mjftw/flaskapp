from webapp import app, db
from webapp.models import User, UserAccess

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'UserAccess': UserAccess}
