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

import json

import deeptracy_core.dal.project.manager as project_manager
from unittest.mock import MagicMock, patch
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
        cls.mock_session = MagicMock()

    def test_get_project_invalid_id(self):
        with self.assertRaises(ValueError):
            project_manager.get_project(None, self.mock_session)

    def test_get_project_not_found(self):
        self.mock_session.query().get.return_value = None
        with self.assertRaises(ValueError):
            project_manager.get_project('123', self.mock_session)

    def test_get_project_found(self):
        self.mock_session.query().get.return_value = Project(id='123', repo='repo')

        project = project_manager.get_project('123', self.mock_session)
        assert project is not None
        assert project.repo == 'repo'

    def test_get_projects_with_empty_table(self):
        self.mock_session.query().all.return_value = None

        projects = project_manager.get_projects(self.mock_session)
        assert projects == []

    def test_get_projects_when_only_one_on_db(self):
        project = Project(id='123', repo='repo')
        self.mock_session.query().all.return_value = [project]

        projects = project_manager.get_projects(self.mock_session)
        assert projects == [project]

    def test_get_projects_when_more_than_one_on_db(self):
        projects_exepected = [Project(id='123', repo='repo'), Project(id='456', repo='repo')]
        self.mock_session.query().all.return_value = projects_exepected
        projects = project_manager.get_projects(self.mock_session)
        assert projects == projects_exepected

    def test_add_project_valid_repo(self):
        repo_url = 'http://repo.com'
        project = project_manager.add_project(repo_url, self.mock_session)
        assert isinstance(project, Project)
        assert project.repo == repo_url
        assert self.mock_session.add.called

    def test_add_project_missing_repo(self):
        with self.assertRaises(AssertionError):
            project_manager.add_project(None, self.mock_session)

        assert not self.mock_session.add.called

    def test_add_project_with_hook_slack_in_kwargs(self):
        data = {
            'repo_auth_type': RepoAuthType.PUBLIC.name,
            'hook_type': ProjectHookType.SLACK.name,
            'hook_data': {
                'webhook_url': 'test_webhook'
            }
        }
        repo_url = 'http://repo.com'
        project = project_manager.add_project(repo_url, self.mock_session, **data)

        assert isinstance(project, Project)
        assert project.repo == repo_url
        assert project.hook_type == ProjectHookType.SLACK.name

        assert json.loads(project.hook_data) == {"webhook_url": "test_webhook"}
        assert self.mock_session.add.called

    def test_add_project_with_hook_email_in_kwargs(self):
        data = {
            'repo_auth_type': RepoAuthType.PUBLIC.name,
            'hook_type': ProjectHookType.EMAIL.name,
            'hook_data': {
                'email': 'mail@mail.com'
            }
        }

        project = project_manager.add_project('http://repo.com', self.mock_session, **data)

        assert project.hook_type == ProjectHookType.EMAIL.name

        assert json.loads(project.hook_data) == {"email": "mail@mail.com"}
        assert self.mock_session.add.called

    def test_add_project_with_invalid_hook_email_in_kwargs(self):
        data = {
            'repo_auth_type': RepoAuthType.PUBLIC.name,
            'hook_type': ProjectHookType.EMAIL.name,
            'hook_data': {
                'invalid': 'mail@mail.com'
            }
        }

        with self.assertRaises(AssertionError):
            project_manager.add_project('http://repo.com', self.mock_session, **data)

    def test_update_project_invalid_auth_type(self):
        with self.assertRaises(AssertionError):
            project_manager.update_project(
                '123',
                self.mock_session,
                repo_auth_type='INVLID_AUTH')

    def test_update_project_invalid_hook_type(self):
        with self.assertRaises(AssertionError):
            project_manager.update_project(
                '123',
                self.mock_session,
                repo_auth_type=RepoAuthType.PUBLIC.name,
                hook_type='INVALID')

    def test_update_project_invalid_hook_data_no_dict(self):
        with self.assertRaises(AssertionError):
            project_manager.update_project(
                '123',
                self.mock_session,
                repo_auth_type=RepoAuthType.PUBLIC.name,
                hook_type=ProjectHookType.SLACK.name,
                hook_data='not_dict')

    def test_update_project_invalid_hook_data_slack_no_webhook(self):
        with self.assertRaises(AssertionError):
            project_manager.update_project(
                '123',
                self.mock_session,
                repo_auth_type=RepoAuthType.PUBLIC.name,
                hook_type=ProjectHookType.SLACK.name,
                hook_data={'missing_key': 'data'})

    @patch('deeptracy_core.dal.project.manager.get_project')
    def test_update_project_valid_no_hook(self, mock_get_project):
        mock_update = MagicMock()
        self.mock_session.query().filter().update = mock_update

        project_manager.update_project(
            '123',
            self.mock_session,
            repo_auth_type=RepoAuthType.PUBLIC.name)

        assert mock_update.called
        mock_update.assert_called_once_with({'repo_auth_type': RepoAuthType.PUBLIC.name})

    @patch('deeptracy_core.dal.project.manager.get_project')
    def test_update_project_valid_hook_slack(self, mock_get_project):
        mock_update = MagicMock()
        self.mock_session.query().filter().update = mock_update

        project_manager.update_project(
            '123',
            self.mock_session,
            repo_auth_type=RepoAuthType.PUBLIC.name,
            hook_type=ProjectHookType.SLACK.name,
            hook_data={'webhook_url': 'http://myslack.com'})

        assert mock_update.called
        mock_update.assert_called_once_with({
            'repo_auth_type': RepoAuthType.PUBLIC.name,
            'hook_type': ProjectHookType.SLACK.name,
            'hook_data': '{"webhook_url": "http://myslack.com"}'
        })

    @patch('deeptracy_core.dal.project.manager.get_project')
    def test_update_project_valid_hook_email(self, mock_get_project):
        mock_update = MagicMock()
        self.mock_session.query().filter().update = mock_update

        project_manager.update_project(
            '123',
            self.mock_session,
            repo_auth_type=RepoAuthType.PUBLIC.name,
            hook_type=ProjectHookType.EMAIL.name,
            hook_data={'email': 'mail@mail.com'})

        assert mock_update.called
        mock_update.assert_called_once_with({
            'repo_auth_type': RepoAuthType.PUBLIC.name,
            'hook_type': ProjectHookType.EMAIL.name,
            'hook_data': '{"email": "mail@mail.com"}'
        })
