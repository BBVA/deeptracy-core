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

import deeptracy_core.dal.scan.manager as scan_manager
from unittest.mock import MagicMock
from deeptracy_core.dal.scan.model import Scan
from tests.unit.base_test import BaseDeeptracyTest


class TestScanManager(BaseDeeptracyTest):
    """Test methods in project manager"""

    @classmethod
    def setUpClass(cls):
        """Mock the database session for all tests"""
        cls.mock_session = MagicMock()

    def setUp(self):
        self.mock_session = MagicMock()

    def test_add_scan_invalid_project_id(self):
        with self.assertRaises(AssertionError):
            scan_manager.add_scan(None, self.mock_session)

    def test_add_scan_valid_scan(self):
        project_id = '123'
        scan_manager.add_scan(project_id, self.mock_session)

        assert self.mock_session.add.called
        kall = self.mock_session.add.call_args
        args, _ = kall
        scan = args[0]
        assert scan.project_id == project_id

    def test_add_scan_with_lang(self):
        project_id = '123'
        lang = 'nodejs'
        scan_manager.add_scan(project_id, self.mock_session, lang=lang)

        assert self.mock_session.add.called
        kall = self.mock_session.add.call_args
        args, _ = kall
        scan = args[0]
        assert scan.project_id == project_id
        assert scan.lang == lang

    def test_get_scan_invalid_scan_id(self):
        with self.assertRaises(AssertionError):
            scan_manager.get_scan(None, self.mock_session)

    def test_get_scan(self):
        scan_id = '123'
        query = MagicMock()
        self.mock_session.query.return_value = query

        scan_manager.get_scan(scan_id, self.mock_session)
        assert query.get.called
        query.get.assert_called_once_with(scan_id)

    def test_update_scan_state_cant_create_scans(self):
        # if a scan without id is passed to update_scan_satate it fails
        scan = Scan()
        with self.assertRaises(ValueError) as exc:
            scan_manager.update_scan_state(scan, scan_manager.ScanState.PENDING, self.mock_session)

        assert 'Cant create scans' in str(exc.exception)

    def test_update_scan_state(self):
        scan_id = '123'
        scan = Scan(id=scan_id, state=scan_manager.ScanState.PENDING)

        scan_manager.update_scan_state(scan, scan_manager.ScanState.INVALID_REPO, self.mock_session)

        scan.state = scan_manager.ScanState.INVALID_REPO.name
        assert self.mock_session.add.called
        self.mock_session.add.assert_called_once_with(scan)

    def test_can_add_scan_limited_by_time(self):
        project_id = "testproject"
        expected_scans = 2

        self.mock_session.query().filter().filter().count.return_value = expected_scans

        num_scans = scan_manager.get_num_scans_in_last_minutes(project_id, 60, self.mock_session)
        self.assertEqual(expected_scans, num_scans)
