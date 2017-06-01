import json
from .mock import Mock
from . import transports

TRANSPORT_MAP = {
    'amqp': transports.AMQPTransport,
    'sql': transports.SQLTransport,
}


class Config:

    transports = None
    files = None

    def __init__(self, config):
        self.transport_settings = config['transports']

        self.mocks = []
        for filename in config['files']:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.mocks.append(Mock(data))

    def setup(self):
        self.transports = {}
        for transport, config in self.transport_settings.items():
            self.transports[transport] = TRANSPORT_MAP[transport](**config)

    def run(self):
        for mock in self.mocks:
            if 'sql' in mock.transport_configs:
                self.transports['sql'].write(mock)
            elif 'amqp' in mock.transport_configs:
                self.transports['amqp'].write(mock)
