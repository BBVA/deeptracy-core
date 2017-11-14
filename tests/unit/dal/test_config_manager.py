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

import deeptracy_core.dal.config.manager as config_manager
from unittest.mock import MagicMock
from tests.unit.base_test import BaseDeeptracyTest


class TestConfigManager(BaseDeeptracyTest):
    """Test methods in project manager"""

    @classmethod
    def setUpClass(cls):
        """Mock the database session for all tests"""
        cls.mock_session = MagicMock()

    def test_save_config_invalid_key(self):
        with self.assertRaises(AssertionError):
            config_manager.save_config(None, 'value', self.mock_session)

    def test_save_config_invalid_value(self):
        with self.assertRaises(AssertionError):
            config_manager.save_config('key', None, self.mock_session)

    def test_save_config_valid(self):
        key = 'key'
        value = 'value'

        self.mock_session.query().get.return_value = None

        config_manager.save_config(key, value, self.mock_session)

        assert self.mock_session.add.called
        kall = self.mock_session.add.call_args
        args, _ = kall
        config = args[0]
        assert config.id == key
        assert config.value == value

    def test_save_dup_config(self):
        key = 'key'
        value = 'value'
        value2 = 'value'

        config_manager.save_config(key, value, self.mock_session)
        config_manager.save_config(key, value2, self.mock_session)

        assert self.mock_session.add.called
        kall = self.mock_session.add.call_args
        args, _ = kall
        config = args[0]
        assert config.value == value2
