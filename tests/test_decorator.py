# -*- coding: utf-8 -*-


from tests.unit.base_test import BaseDeeptracyTest
from deeptracy_core.dal.database import db, Base


class TestUtilsValidRepo(BaseDeeptracyTest):

    def test_init_engine_creates_project_table(self):
        db.init_engine()
        print(Base.metadata.tables.keys())