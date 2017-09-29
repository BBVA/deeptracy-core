# -*- coding: utf-8 -*-

import deeptracy_core.dal.plugin.manager as plugin_manager
from unittest.mock import MagicMock
from deeptracy_core.dal.plugin.model import Plugin
from tests.unit.base_test import BaseDeeptracyTest
from tests.unit.mock_db import MockDeeptracyDBEngine


class TestPluginManager(BaseDeeptracyTest):
    """Test methods in scan manager"""

    @classmethod
    def setUpClass(cls):
        """Mock the database engine for all tests"""
        plugin_manager.db = MockDeeptracyDBEngine()
        cls.db = plugin_manager.db

    def setUp(self):
        self.db.Session.query._ret_val = None

    def test_deactivate_all_plugins(self):
        session = MagicMock()
        query = MagicMock()
        session.query.return_value = query
        plugin_manager.deactivate_all_plugins(session)

        assert query.update.called
        query.update.assert_called_once_with({Plugin.active: False})

    def test_add_or_activate_plugin_existing_plugin(self):
        plugin_name = 'plugin_name'
        plugin_lang = 'plugin_lang'
        session = MagicMock()
        query = MagicMock()
        plugin = Plugin(name=plugin_name, lang=plugin_lang, active=False)
        session.query().filter.return_value = query
        query.first.return_value = plugin

        plugin_manager.add_or_activate_plugin(plugin_name, plugin_lang, session)

        assert session.add.called
        session.add.assert_called_once_with(plugin)

    def test_add_or_activate_plugin_exis_plugin(self):
        plugin_name = 'plugin_name'
        plugin_lang = 'plugin_lang'
        session = MagicMock()
        query = MagicMock()
        session.query().filter.return_value = query
        query.first.return_value = None

        plugin_manager.add_or_activate_plugin(plugin_name, plugin_lang, session)

        assert session.add.called
        kall = session.add.call_args
        args, _ = kall
        plugin = args[0]
        assert plugin.active is True
        assert plugin.name is plugin_name
        assert plugin.lang is plugin_lang
