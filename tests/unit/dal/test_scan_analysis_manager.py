# -*- coding: utf-8 -*-

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
