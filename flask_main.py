from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces
from werkzeug import serving

from webapp import app, db, ssl_ctx
from webapp.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

def main():
    ipaddr = netifaces.ifaddresses('wlan0')[AF_INET][0]['addr']
    serving.run_simple(
        application=app,
        hostname=ipaddr,
        port=8443,
        threaded=True,
        ssl_context=ssl_ctx)

if __name__ == "__main__":
    main()