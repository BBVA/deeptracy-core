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

from datetime import datetime
from unittest.mock import MagicMock, Mock
from tests.unit.base_test import BaseDeeptracyTest

from deeptracy_core.dal.scan_vul.manager import add_scan_vul
from deeptracy_core.dal.scan_dep.model import ScanDep


class TestScanVulManager(BaseDeeptracyTest):
    """Test methods in scan vul manager"""

    @classmethod
    def setUpClass(cls):
        """Mock the database session for all tests"""
        cls.mock_session = MagicMock()

    def setUp(self):
        self.mock_session.reset_mock()

    def test_add_scan_vul_scan_id_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_vul(None, 'panda', '6.23.00', [], self.mock_session)

    def test_add_scan_vul_library_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_vul('123', None, '6.23.00', [], self.mock_session)

    def test_add_scan_vul_version_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_vul('123', 'panda', None, [], self.mock_session)

    def test_add_scan_vul_vulnerabilities_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_vul('123', 'panda', '6.23.00', None, self.mock_session)

    def test_add_vul_valid(self):
        scan_id = '123'
        library = 'panda'
        version = '6.23.00'

        add_scan_vul(scan_id, library, version, [], self.mock_session)

        assert self.mock_session.add.called
        kall = self.mock_session.add.call_args
        args, _ = kall
        scan_vul = args[0]

        assert scan_vul.scan_id == scan_id
        assert scan_vul.library == library
        assert scan_vul.version == version
