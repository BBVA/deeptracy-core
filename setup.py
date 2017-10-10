#!/usr/bin/env python

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    readme = f.read()

requirements = [str(ir.req) for ir in parse_requirements(
    'requirements.txt',
    session=PipSession())]

test_requirements = [str(ir.req) for ir in parse_requirements(
    'requirements_test.txt', session=PipSession())]


setup(
    name='deeptracy_core',
    version='0.0.13',
    author='BBVA',
    url="https://github.com/BBVA/deeptracy-core",
    description='Deeptracy Dependency Checker',
    long_description=readme,
    packages=find_packages(),
    keywords='deeptracy core',
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
