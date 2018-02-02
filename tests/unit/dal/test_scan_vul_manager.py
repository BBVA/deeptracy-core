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
from unittest import mock
from unittest.mock import MagicMock
from tests.unit.base_test import BaseDeeptracyTest

from deeptracy_core.dal.scan_vul.manager import add_scan_vuln
# import deeptracy_core.dal.scan_vul.manager
# deeptracy_core.dal.scan_vul.manager.get_or_create_vuln_in_scan = lambda x,y: {'x':x, 'y':y}


class TestScanVulManager(BaseDeeptracyTest):
    """Test methods in scan vul manager"""

    @classmethod
    def setUpClass(cls):
        """Mock the database session for all tests"""
        cls.mock_session = MagicMock()

    def setUp(self):
        self.mock_session.reset_mock()

    def test_add_scan_vul_scan_dep_id_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_vuln(None, '123', 'nodejs', 'cpe:demo', [], self.mock_session)

    def test_add_scan_vul_scan_id_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_vuln('11', None, 'nodejs', 'cpe:demo', [], self.mock_session)

    def test_add_scan_vul_lang_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_vuln('11', '123', None, 'cpe:demo', [], self.mock_session)

    def test_add_scan_vul_cpe_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_vuln('11', '123', 'nodejs', None, [], self.mock_session)

    def test_add_scan_vul_cves_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_vuln('11', '123', 'nodejs', 'cpe:demo', None, self.mock_session)

    # @mock.patch('deeptracy_core.dal.scan_vul.manager.add_scan_vuln', return_value={'id': '11211'})
    # def test_add_vul_valid(self, mock_get_or_create_vuln):
    #     scan_dep_id = '11'
    #     scan_id = '123'
    #     lang = 'nodejs'
    #     cpe = 'cpe:demo'
    #     cves = [{"cve": "CVE-2001-2323", "score": 5}]
    #     self.mock_session.attach_mock(mock_get_or_create_vuln, 'get_or_create_vuln')
    #     add_scan_vuln(scan_dep_id, scan_id, lang, cpe, cves, self.mock_session)
    #
    #     assert self.mock_session.add.called
    #     kall = self.mock_session.add.call_args
    #     args, _ = kall
    #     scan_vul = args[0]
    #
    #     assert scan_vul.scan_id == scan_id
    #     assert scan_vul.lang == lang
    #     assert scan_vul.cpe == cpe
    #     assert scan_vul.max_score == 5
