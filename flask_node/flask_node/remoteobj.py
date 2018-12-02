from flask import Flask, request
import inspect


class RxClass():
    def __init__(self, name=None, host='localhost', port='5000', debug=False):
        name = name or '{}_api'.format(self.__class__.__name__)
        self.app = Flask(name)
        self.host = host or 'localhost'
        self.port = port or '5000'
        self.debug = debug

        self.start_time = None
        if not hasattr(self, 'methods'):
            self.methods = ['GET']

        def get_method_call(m):
            return str((m, inspect.getargspec(getattr(self, m)).args[1:]))

        def get_methods():
            method_names = [m[0] for m in inspect.getmembers(self, predicate=inspect.ismethod)]
            method_names = filter(lambda m: not (m.startswith('_') or m == 'run_api'), method_names)
            return str([get_method_call(m)for m in method_names])

        self.app.add_url_rule(
            '/',
            '/',
            view_func=get_methods,
            methods=['GET'])

        @self.app.route('/<m>', methods=['GET', 'POST'])
        def api_method(m):
            func = getattr(self, m)
            al = inspect.getargspec(func).args[1:] or []
            if request.method == 'GET':
                return get_method_call(m)

            dl = inspect.getargspec(func).defaults or []
            args_defs = [l for l in al[:len(al)-len(dl)]] + list(zip(al[::-1], dl[::-1]))[::-1]

            args = []
            for a in args_defs:
                if isinstance(a, tuple):
                    args.append(request.args.get(a[0], default=a[1]))
                else:
                    args.append(request.args.get(a))

            return str(func(*args))


    def run_api(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)