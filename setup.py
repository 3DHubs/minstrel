#!/usr/bin/env python
import os
from setuptools import setup, find_packages

# Maintain version in a single location and read it from there
path = os.path.join(os.path.dirname(__file__), 'VERSION')
with open(path) as version_file:
    version = version_file.read().strip()
assert version

setup(
    name='Minstrel',
    version=version,
    description='Manage, generate, and apply mocks.',
    author='Martijn Arts',
    author_email='martijn@3dhubs.com',
    url='https://github.com/3DHubs/minstrel',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['minstrel'],
    install_requires=[
        'frozendict',
        'jsonpatch',
        'click',
        'kombu',
        'psycopg2',
        'SQLAlchemy',
        'mypy_extensions',
    ],
    entry_points={
        'console_scripts': [
            'minstrel = minstrel.cli:minstrel'
        ]
    }
)
