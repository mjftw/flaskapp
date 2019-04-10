from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces
import threading
from werkzeug import serving

from webapp import app, db, ssl_ctx
from webapp.models import User, SensorData
from webapp.logger import SensorLogger


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'SensorData': SensorData}

def main():
    ipaddr = netifaces.ifaddresses('wlan0')[AF_INET][0]['addr']

    if 'NODEURL_TEMP_LOGGER_FV' in app.config:
        __, fv_temp_tx_ip, fv_temp_tx_port = tuple(
            app.config['NODEURL_TEMP_LOGGER_FV'].split(':'))

        temp_logger = SensorLogger( 
            tx_ip=ipaddr, 
            tx_port=5010, 
            sample_period_s=60, 
            name='TempSensorLogger', 
            sensor_db_name='brew-fridge-temperature', 
            sensor_ip='192.168.0.210', 
            sensor_port=5010, 
            sensor_read_method='get_value' 
        )
        t = threading.Thread(target=temp_logger.run_api)
        t.start()

    serving.run_simple(
        application=app,
        hostname=ipaddr,
        port=8443,
        threaded=True,
        ssl_context=ssl_ctx)

if __name__ == "__main__":
    main()