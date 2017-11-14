# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    version='0.0.25',
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
