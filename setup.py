#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    readme = f.read()


setup(
    name='deeptracy_core',
    version='0.0.1',
    author='BBVA',
    description=readme,
    long_description=readme,
    packages=find_packages(),
    keywords='deeptracy core',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
