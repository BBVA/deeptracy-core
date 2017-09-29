# -*- coding: utf-8 -*-
import sqlalchemy

from unittest import mock
from tests.unit.base_test import BaseDeeptracyTest
from deeptracy_core.dal.database import db, Base


class TestStartScan(BaseDeeptracyTest):

    @mock.patch.object(sqlalchemy, 'create_engine')
    def test_module_registers_all_modules_in_metadata(self, mock_create_engine):
        """After initialization all models needs to exist in the metadata"""
        db.init_engine()
        assert 'project' in Base.metadata.tables.keys()
        assert 'scan' in Base.metadata.tables.keys()
        assert 'plugin' in Base.metadata.tables.keys()
        assert 'scan_analysis' in Base.metadata.tables.keys()
        assert 'scan_analysis_vulnerability' in Base.metadata.tables.keys()
        assert 'scan_vulnerability' in Base.metadata.tables.keys()

    @mock.patch('deeptracy_core.dal.database.Base')
    @mock.patch('deeptracy_core.dal.database.database_exists', return_value=False)
    @mock.patch.object(sqlalchemy, 'create_engine')
    def test_after_init_engine_metadata_should_create_all_models(self,
                                                                 mock_database_exists,
                                                                 mock_create_engine,
                                                                 mock_base):
        """After initialization metadata should create all models"""
        db.init_engine()
        assert mock_base.metadata.create_all.called
