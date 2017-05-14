"""A PostgreSQL mocking and things library."""

import json


def _load_file(filename):
    with open(filename, 'r') as data_file:
        return json.loads(data_file)


def generate_mocks(data):
    pass
