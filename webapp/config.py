import os
import configparser


basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    def __init__(self):
        self.config_file = os.environ.get('FLASK_CONFIG') or os.path.join(basedir, 'config.ini')
        self.config = None

        # Read in any config in config file
        if os.path.exists(self.config_file):
            print('Reading config file {}'.format(self.config_file))
            self.config = configparser.ConfigParser()
            self.config.read(self.config_file)
            for section in self.config:
                for var in self.config[section]:
                    var = var.upper()
                    value = self.config[section][var]
                    print('Setting {} = {} (from {})'.format(var, value, self.config_file))
                    setattr(self, var, value)
                    os.environ[var] = str(value)

        # Find other required config if not already found
        self.source_config('SECRET_KEY', "ep2gz+zx)edg2LM{")
        self.source_config('SQLALCHEMY_DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'app.db'))
        self.source_config('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        self.source_config('SSL_CERT', os.path.join(basedir, 'cert.pem'))
        self.source_config('SSL_KEY', os.path.join(basedir, 'privkey.pem'))

    def source_config(self, name, default=None, export_env=True):
        if hasattr(self, name):
            return

        value = default
        if os.environ.get(name):
            value = os.environ.get(name)
            print('Setting {} = {} (from environment variable)'.format(name, value))
        else:
            print('Setting {} = {} (default value): '.format(name, default))

        setattr(self, name, value)
        if export_env:
            os.environ[name] = str(value)
