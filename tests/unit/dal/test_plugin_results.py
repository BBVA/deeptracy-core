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

import pytest

from deeptracy_core import PluginResult, PluginSeverityEnum


def test_plugin_result_ok():
    p = PluginResult('retire', '1.0.1', PluginSeverityEnum.MEDIUM)

    assert p.library == 'retire'
    assert p.version == '1.0.1'
    assert p.severity == 2


def test_plugin_result_invalid_library_type():

    with pytest.raises(AssertionError):
        PluginResult(1, '1.0.1', PluginSeverityEnum.MEDIUM)


def test_plugin_result_invalid_version_type():

    with pytest.raises(AssertionError):
        PluginResult('retire', 1, PluginSeverityEnum.MEDIUM)


def test_plugin_result_invalid_serverity_type():

    with pytest.raises(AssertionError):
        PluginResult('retire', '1.0.1', 'asdf')


def test_plugin_result_invalid_summary_type():

    with pytest.raises(AssertionError):
        PluginResult('retire',
                     '1.0.1',
                     PluginSeverityEnum.HIGH,
                     summary=1)


def test_plugin_result_invalid_advisory_type():

    with pytest.raises(AssertionError):
        PluginResult('retire',
                     '1.0.1',
                     PluginSeverityEnum.HIGH,
                     summary=1)


def test_plugin_result_has_to_dict():

    plugin_result = PluginResult('retire',
                                 '1.0.1',
                                 PluginSeverityEnum.HIGH)

    plugin_result_dict = plugin_result.to_dict()
    assert plugin_result_dict.get('library') == 'retire'
    assert plugin_result_dict.get('version') == '1.0.1'
    assert plugin_result_dict.get('severity') == PluginSeverityEnum.HIGH.value
