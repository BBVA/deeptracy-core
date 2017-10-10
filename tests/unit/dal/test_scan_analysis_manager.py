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

import deeptracy_core.dal.scan_analysis.manager as scan_analysis_manager
from unittest.mock import MagicMock
from deeptracy_core.dal.plugin_results import PluginResult, PluginSeverityEnum
from tests.unit.base_test import BaseDeeptracyTest


class TestScanManager(BaseDeeptracyTest):
    """Test methods in scan_analysis_manager"""

    def test_add_scan_vulnerabilities_results_invalid_scan_id(self):
        mock_session = MagicMock()
        with self.assertRaises(AssertionError):
            scan_analysis_manager.add_scan_vulnerabilities_results(None, [], mock_session)

    def test_add_scan_vulnerabilities_results_empty_results(self):
        mock_session = MagicMock()
        scan_analysis_manager.add_scan_vulnerabilities_results('123', [], mock_session)

        assert mock_session.add.call_count == 0

    def test_add_scan_vulnerabilities_results(self):
        mock_session = MagicMock()
        result1 = PluginResult(library='lib', version='1', severity=PluginSeverityEnum.CRITICAL)
        result2 = PluginResult(library='lib', version='1', severity=PluginSeverityEnum.CRITICAL)
        result3 = PluginResult(library='lib', version='1', severity=PluginSeverityEnum.CRITICAL)

        scan_analysis_manager.add_scan_vulnerabilities_results('123', [result1, result2, result3], mock_session)

        assert mock_session.add.call_count == 3
