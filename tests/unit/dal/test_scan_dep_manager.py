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

from deeptracy_core.dal.scan_dep.manager import add_scan_dep, add_scan_deps, compare_scan_deps
from deeptracy_core.dal.scan_dep.model import ScanDep


class TestScanManager(BaseDeeptracyTest):
    """Test methods in scan dep manager"""

    @classmethod
    def setUpClass(cls):
        """Mock the database session for all tests"""
        cls.mock_session = MagicMock()

    def setUp(self):
        self.mock_session.reset_mock()

    def test_add_scan_dep_scan_id_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_dep(None, 'dep', datetime.now(), self.mock_session)

    def test_add_scan_dep_raw_dep_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_dep('scan_id', None, datetime.now(), self.mock_session)

    def test_add_scan_dep_found_at_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_dep('scan_id', 'dep', None, self.mock_session)

    def test_add_scan_dep_valid(self):
        scan_id = '123'
        dep = 'raw_dep'
        dt = datetime.now()
        add_scan_dep(scan_id, dep, dt, self.mock_session)

        assert self.mock_session.add.called
        kall = self.mock_session.add.call_args
        args, _ = kall
        scan_dep = args[0]
        assert scan_dep.scan_id == scan_id
        assert scan_dep.raw_dep == dep
        assert scan_dep.found_at == dt

    def test_add_scan_deps_scan_id_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_deps(None, ['dep'], datetime.now(), self.mock_session)

    def test_add_scan_deps_raw_dep_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_deps('scan_id', None, datetime.now(), self.mock_session)

    def test_add_scan_deps_found_at_mandatory(self):
        with self.assertRaises(AssertionError):
            add_scan_deps('scan_id', ['dep'], None, self.mock_session)

    def test_add_scan_deps_valid(self):
        scan_id = '123'
        deps = ['raw_dep', 'raw_dep1', 'raw_dep2']
        dt = datetime.now()
        add_scan_deps(scan_id, deps, dt, self.mock_session)

        assert self.mock_session.add_all.called
        kall = self.mock_session.add_all.call_args
        args, _ = kall
        scan_dep_list = args[0]
        for idx, scan_dep in enumerate(scan_dep_list):
            assert scan_dep.scan_id == scan_id
            assert scan_dep.raw_dep == deps[idx]
            assert scan_dep.found_at == dt

    def test_compare_scan_deps_equals(self):
        list1 = [ScanDep(raw_dep='el1')]
        list2 = [ScanDep(raw_dep='el1')]
        query_all = Mock()
        query_all.side_effect = [list1, list2]

        self.mock_session.query().filter().all = query_all

        equals = compare_scan_deps('scan_id', 'scan_id2', self.mock_session)
        self.assertTrue(equals)

    def test_compare_scan_deps_not_equals(self):
        list1 = [ScanDep(raw_dep='el1')]
        list2 = [ScanDep(raw_dep='el2')]
        query_all = Mock()
        query_all.side_effect = [list1, list2]

        self.mock_session.query().filter().all = query_all

        equals = compare_scan_deps('scan_id', 'scan_id2', self.mock_session)
        self.assertFalse(equals)

    def test_compare_scan_deps_not_equals_more_elements_first(self):
        list1 = [ScanDep(raw_dep='el1'), ScanDep(raw_dep='el2')]
        list2 = [ScanDep(raw_dep='el1')]
        query_all = Mock()
        query_all.side_effect = [list1, list2]

        self.mock_session.query().filter().all = query_all

        equals = compare_scan_deps('scan_id', 'scan_id2', self.mock_session)
        self.assertFalse(equals)

    def test_compare_scan_deps_not_equals_more_elements_second(self):
        list1 = [ScanDep(raw_dep='el1')]
        list2 = [ScanDep(raw_dep='el1'), ScanDep(raw_dep='el2')]
        query_all = Mock()
        query_all.side_effect = [list1, list2]

        self.mock_session.query().filter().all = query_all

        equals = compare_scan_deps('scan_id', 'scan_id2', self.mock_session)
        self.assertFalse(equals)
