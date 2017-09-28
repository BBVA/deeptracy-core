# -*- coding: utf-8 -*-

from unittest import mock
from tests.unit.base_test import BaseDeeptracyTest
import deeptracy_core.dal.database as database
from deeptracy_core.dal.database import db, Base


class TestStartScan(BaseDeeptracyTest):

    def test_after_init_engine_tables_exists_in_metadata(self):
        """After initialization all models needs to exist in the metadata"""
        database.DATABASE_URI = 'sqlite:///:memory:'
        db.init_engine()
        assert 'project' in Base.metadata.tables.keys()
        assert 'scan' in Base.metadata.tables.keys()
        assert 'plugin' in Base.metadata.tables.keys()
        assert 'scan_analysis' in Base.metadata.tables.keys()
        assert 'scan_analysis_vulnerability' in Base.metadata.tables.keys()
        assert 'scan_vulnerability' in Base.metadata.tables.keys()

    @mock.patch('deeptracy_core.dal.database.Base')
    def test_after_init_engine_metadata_should_create_all_models(self, mock_base):
        """After initialization metadata should create all models"""
        database.DATABASE_URI = 'sqlite:///:memory:'
        db.init_engine()
        assert mock_base.metadata.create_all.called
