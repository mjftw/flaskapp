import json
import requests
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from webapp import app
from webapp import db
from webapp.models import SensorData


@app.route('/brewcontrol/node_api_call')
@login_required
def node_api_call():
    if not current_user.is_admin:
        return 'Err not admin', 401

    url = request.args.get('url')
    method = request.args.get('method')
    method_args = {name[len('arg_'):]: request.args[name] for name in request.args
        if name.startswith('arg_') and request.args[name]}
    if url and method:
        r = requests.post(url + '/' + method, params=method_args or None)
        return r.text or ''
    else:
        return 'Err invalid call', 404