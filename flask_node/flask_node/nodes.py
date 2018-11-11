'''
A Node is a small standalone flask server, which is able to communicate
with other nodes in order to perform some task.
Nodes communicate with each other by passing JSON messages over a
RESTful API.
Nodes can represent physical entities, such as a temperature sensor,
or a light switch, or they can be virtual, and represent something
like a PID controller.
'''

from flask import jsonify, Flask, request

class Node():
    '''
    The base class inherited by all node classes
    Handles the message sending and recieving functionality.
    I.e. Handles the communication between nodes
    Uses JSON to pass messages
    '''
    def __init__(self, name, host=None, port=None, debug=None, path=None):
        self.app = Flask(name)
        self.host = host
        self.port = port
        self.debug = debug
        self.path = path or '/'

        self.start_time = None
        if not hasattr(self, 'methods'):
            self.methods = ['GET']

        self.app.add_url_rule(
            self.path,
            'api',
            view_func=self.api,
            methods=self.methods)

    @property
    def info(self):
        info = {
            'name': self.app.name,
            'type': self.__class__.__name__,
            'url': "{}:{}{}".format(
                self.host or 'localhost',
                self.port,
                self.path)
        }
        return info

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)

    def message(self, body=None, **kwargs):
        content = {}

        content['header'] = self.info
        if body:
            content['body'] = body

        if kwargs:
            content['kwargs'] = kwargs

        return jsonify(content)

    def api(self):
        return self.message()


class StemNode(Node):
    '''
    Represents a node that can have child nodes decending from it.
    Holds a map that of the nodes below it.
    Is able to send parts of this map to child stem nodes in order to
    configure them.
    E.g.
      Child node --- Stem node
                    /
         ... --- Child node
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class SensorNode(Node):
    '''
    Represents a generic sensor in the system
    A way of reading the value of something. E.g. Temperature
    '''

    def __init__(self, *args, **kwargs):
        self.mock_reading = 0
        super().__init__(*args, **kwargs)

    def api(self):
        if request.method == 'GET':
            return self.message({'sample': self.read_sensor()})

    def read_sensor(self):
        '''
        This function should be overridden with something that reads
        the value of the sensor, and returns it.
        '''
        self.mock_reading += 1
        return self.mock_reading

class ActionNode(Node):
    '''
    Represents a generic actuator in the system
    A way of causing an action. E.g. A plug controller
    '''

    def __init__(self, *args, **kwargs):
        self.methods = ['GET', 'POST']
        self.value = None
        super().__init__(*args, **kwargs)

    def api(self):
        if request.method == 'GET':
            return self.message({'value': self.value})
        elif request.method == 'POST':
            value = request.args.get('value')
            if value is None or value == '':
                return '', 400

            self.set_value(request.args.get('value'))
            return str(self.value)

    def set_value(self, value):
        '''
        This function should be overwritten with functionality to trigger
        an action. E.g. Turn on a plug
        This function should update self.value to refelect the change made
        @value: The value to set. E.g. On/Off for a plug
        '''
        self.value = value
        print(value)

class ControlNode(StemNode):
    '''
    Represents a controller in the system.
    The controller has sensors, actuators, and a control function
    that tells it how to use the sensor information to control the
    actuators.
    E.g. A PID temperature controller
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sensors = []
        self.actuators = []

    def control_func(self):
        '''
        The feedback function to use in the control loop.
        E.g. The control function for a PID controller
        '''
        pass

