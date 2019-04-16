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

@app.route('/api/get_data_in_range')
@login_required
def get_data_in_range():
    if not current_user.is_admin:
        return 'Err not admin', 401

    date_format = '%Y-%m-%d %H:%M:%S'

    print(datetime.strftime(datetime.now(), date_format))

    start = request.args.get('start')
    end = request.args.get('end')
    sensor_name = request.args.get('sensor_name')

    if not start or not end or not sensor_name:
        return 'Err invalid call', 400

    start_date = datetime.strptime(start, date_format)
    end_date = datetime.strptime(end, date_format)

    data = [
        {
            'x': datetime.strftime(d.date, date_format),
            'y': d.value
        } 
        for d in db.session.query(SensorData).filter(
            SensorData.sensor_name==sensor_name).filter(
                SensorData.date.between(start_date, end_date)).all()
    ]

    return json.dumps(data), 200
   