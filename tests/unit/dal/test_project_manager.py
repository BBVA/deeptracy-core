# -*- coding: utf-8 -*-
import pickle
import base64

import deeptracy_core.dal.project.manager as project_manager
from unittest.mock import MagicMock
from deeptracy_core.dal.project.model import Project
from deeptracy_core.dal.project.repo_auth import RepoAuth, RepoAuthType
from tests.unit.base_test import BaseDeeptracyTest
from tests.unit.mock_db import MockDeeptracyDBEngine


class TestProjectManager(BaseDeeptracyTest):
    """Test methods in project manager"""

    @classmethod
    def setUpClass(cls):
        """Mock the database engine for all tests"""
        project_manager.db = MockDeeptracyDBEngine()
        cls.db = project_manager.db

    def setUp(self):
        self.db.Session.query._ret_val = None

    def test_get_project_invalid_id(self):
        with self.assertRaises(ValueError):
            project_manager.get_project(None, self.db.Session())

    def test_get_project_not_found(self):
        with self.assertRaises(ValueError):
            project_manager.get_project('123', self.db.Session())

    def test_get_project_found(self):
        # mock the return value
        self.db.Session.query._ret_val = Project(id='123', repo='repo')

        project = project_manager.get_project('123', self.db.Session())
        assert project is not None
        assert project.repo == 'repo'

    def test_add_project_valid_repo(self):
        repo_url = 'http://repo.com'
        session = MagicMock()
        project = project_manager.add_project(repo_url, session)
        assert isinstance(project, Project)
        assert project.repo == repo_url
        assert session.add.called

    def test_add_project_missing_repo(self):
        session = MagicMock()
        with self.assertRaises(AssertionError):
            project_manager.add_project(None, session)

        assert not session.add.called

    def test_add_project_with_auth_is_b64encoded(self):
        repo_url = 'http://repo.com'
        session = MagicMock()
        repo_auth = RepoAuth(pkey_str='=-private_key-=')

        project_manager.add_project(repo_url, session, repo_auth_type=RepoAuthType.PRIVATE_KEY, repo_auth=repo_auth)
        assert session.add.called
        kall = session.add.call_args
        args, _ = kall
        project = args[0]

        # assert that the auth has been pickled and b64 encoded
        pickled = pickle.dumps(repo_auth.to_dict())
        encoded_auth = base64.b64encode(pickled)
        assert project.repo_auth == encoded_auth

        # assert that the auth can be unpiclked and b64 decoded
        decoded_auth = base64.b64decode(encoded_auth)
        unpickled = pickle.loads(decoded_auth)
        assert repo_auth.to_dict() == unpickled
