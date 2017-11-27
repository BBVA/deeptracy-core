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

import pickle
import base64
import json

import deeptracy_core.dal.project.manager as project_manager
from unittest.mock import MagicMock
from deeptracy_core.dal.project.model import Project
from deeptracy_core.dal.project.repo_auth import RepoAuth, RepoAuthType
from deeptracy_core.dal.project.project_hooks import ProjectHookType
from tests.unit.base_test import BaseDeeptracyTest
from tests.unit.mock_db import MockDeeptracyDBEngine


class TestProjectManager(BaseDeeptracyTest):
    """Test methods in project manager"""

    @classmethod
    def setUpClass(cls):
        """Mock the database engine for all tests"""
        project_manager.db = MockDeeptracyDBEngine()
        cls.db = project_manager.db
        cls.test_name = 'name'
        cls.test_repo = 'http://repo.com'
        cls.test_projects = [Project(id='123', name=cls.test_name, repo=cls.test_repo),
                             Project(id='456', name=cls.test_name, repo=cls.test_repo)]

    def setUp(self):
        self.db.Session.query._ret_val = None

    def test_get_project_invalid_id(self):
        with self.assertRaises(ValueError):
            project_manager.get_project(None, self.db.Session())

    def test_get_project_not_found(self):
        with self.assertRaises(ValueError):
            project_manager.get_project(self.test_projects[0].id, self.db.Session())

    def test_get_project_found(self):
        # mock the return value
        self.db.Session.query._ret_val = self.test_projects[0]

        project = project_manager.get_project(self.test_projects[0].id, self.db.Session())
        assert project is not None
        assert project.repo == self.test_repo
        assert project.name == self.test_name

    def test_get_projects_with_empty_table(self):
        # mock the return value
        self.db.Session.query._ret_val = []

        projects = project_manager.get_projects(self.db.Session())
        assert projects is not []

    def test_get_projects_when_only_one_on_db(self):
        # mock the return value
        self.db.Session.query._ret_val = [self.test_projects[0]]

        projects = project_manager.get_projects(self.db.Session())
        assert projects is not [self.test_projects[0]]

    def test_get_projects_when_more_than_one_on_db(self):
        # mock the return value
        self.db.Session.query._ret_val = self.test_projects

        projects = project_manager.get_projects(self.db.Session())
        assert projects is not self.test_projects

    def test_add_project_valid_repo(self):
        session = MagicMock()
        project = project_manager.add_project(self.test_repo, self.test_name, session)
        assert isinstance(project, Project)
        assert project.repo == self.test_repo
        assert project.name == self.test_name
        assert session.add.called

    def test_add_project_missing_repo(self):
        session = MagicMock()
        with self.assertRaises(AssertionError):
            project_manager.add_project(None, self.test_name, session)

        assert not session.add.called

    def test_add_project_missing_name(self):
        session = MagicMock()
        with self.assertRaises(AssertionError):
            project_manager.add_project(self.test_repo, None, session)

        assert not session.add.called

    def test_add_project_with_hooks_in_kwargs(self):
        session = MagicMock()
        data = {
            'repo_auth_type': RepoAuthType.PUBLIC.name,
            'hook_type': ProjectHookType.SLACK.name,
            'hook_data': {
                'webhook_url': 'test_webhook'
            }
        }
        repo_url = 'http://repo.com'
        name = 'name'
        project = project_manager.add_project(repo_url, name, session, **data)

        assert isinstance(project, Project)
        assert project.repo == repo_url
        assert project.name == name
        assert project.hook_type == ProjectHookType.SLACK.name

        assert json.loads(project.hook_data) == {"webhook_url": "test_webhook"}
        assert session.add.called
