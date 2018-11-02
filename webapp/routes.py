from flask import render_template

from webapp import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Merlin'}
    return render_template('index.html', title='Home', user=user)