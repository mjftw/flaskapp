from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces

from webapp import app, db
from webapp.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

def main():
    ipaddr = netifaces.ifaddresses('wlan0')[AF_INET][0]['addr']
    # app.run(ssl_context='adhoc')
    app.run(debug=True, host=ipaddr, port=5000)

if __name__ == "__main__":
    main()