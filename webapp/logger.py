from datetime import datetime

from flask_node.remoteobj import TxClassLooping, RxReadSimple

from webapp.models import SensorData
from webapp import db

class SensorLogger(TxClassLooping, RxReadSimple):
    def __init__(self, tx_ip, tx_port, sample_period_s, name, sensor_db_name,
            sensor_ip, sensor_port, sensor_read_method, sensor_read_args=None,
            log_repeated_data=False):
        RxReadSimple.__init__(self,
            remote_host=sensor_ip,
            remote_port=sensor_port,
            remote_method=sensor_read_method,
            remote_args=sensor_read_args or (),
            callback=self._save_to_db
        )
        TxClassLooping.__init__(self,
            loop_method_name='read',
            loop_sleep=sample_period_s,
            pause_sleep=1,
            name=name,
            host=tx_ip,
            port=tx_port
        )

        self.sensor_db_name = sensor_db_name
        self.log_repeated_data = log_repeated_data

    @property
    def sample_period_s(self):
        return 

    def _save_to_db(self, value):
        last_value = db.session.query(
            SensorData).order_by(SensorData.id.desc()).first().value
        print('new [{}], last[{}]'.format(value, last_value))
        if value != last_value or self.log_repeated_data:
            data = SensorData(
                sensor_name=self.sensor_db_name,
                value=value,
                date=datetime.now())

            db.session.add(data)
            db.session.commit()

    @property
    def sample_period(self):
        return self._loop_sleep