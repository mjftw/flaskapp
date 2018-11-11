'''
A Node is a small standalone flask server, which is able to communicate
with other nodes in order to perform some task.
Nodes communicate with each other by passing JSON messages over a
RESTful API.
Nodes can represent physical entities, such as a temperature sensor,
or a light switch, or they can be virtual, and represent something
like a PID controller.
'''
import datetime

from flask import jsonify, Flask, request

class Node():
    '''
    The base class inherited by all node classes
    Handles the message sending and recieving functionality.
    I.e. Handles the communication between nodes
    Uses JSON to pass messages
    '''
    def __init__(self, name, host=None, port=None, debug=None):
        self.app = Flask(name)
        self.host = host
        self.port = port
        self.debug = debug

        self.start_time = None
        self.api_methods = ['GET', 'POST']

        self.app.add_url_rule(
            '/api',
            'api',
            view_func=self.api,
            methods=self.api_methods)

    @property
    def info(self):
        now = datetime.datetime.now()
        uptime = now - self.start_time
        info = {
            'name': self.app.name,
            'type': self.__class__.__name__,
            'host': self.host,
            'port': self.port,
            'uptime': str(uptime),
            'request_time': str(now)
        }
        return info

    def run(self):
        self.start_time = datetime.datetime.now()
        self.app.run(host=self.host, port=self.port, debug=self.debug)

    def message(self, body=None, **kwargs):
        content = {}

        content['header'] = self.info
        if body:
            content['body'] = body

        if kwargs:
            content['kwargs'] = kwargs

        return jsonify(content)

    def jsonify(self):
        '''
        Defines a common header for all messages passed by nodes
        '''

    def api(self):
        if request.method == 'GET':
            msg = self.message(method='GET')
        elif request.method == 'POST':
            msg = self.message(method='POST')

        return msg


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
        super().__init__(*args, **kwargs)
        self.values = None

    def read(self, range=None):
        '''
        Returns a list of sensor values.
        @range: A range of sensor values to read. If None, returns all
        '''

    def flush(self, range=None):
        '''
        Flushes a range of sensor values from the buffer
        @range: The range of sensor values to remove. If None, flushes all
        '''

class ActionNode(Node):
    '''
    Represents a generic actuator in the system
    A way of causing an action. E.g. A plug controller
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do(self, value):
        '''
        Trigger an action. E.g. Turn on a plug
        @value: The value to set. E.g. On/Off for a plug
        '''
        pass

    def read(self):
        '''
        Get the state of the node, if it has one.
        E.g. The state of a switch that this node controls
        '''
        pass


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

