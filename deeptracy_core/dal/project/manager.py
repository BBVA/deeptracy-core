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

"""Manager function to deal with Project model"""
import base64
import pickle
import json
import logging

from sqlalchemy.orm import Session
from deeptracy_core.dal.project.model import Project
from deeptracy_core.dal.project.repo_auth import RepoAuthType, RepoAuth
from deeptracy_core.dal.project.project_hooks import ProjectHookType

log = logging.getLogger(__name__)


def add_project(
        repo: str, session: Session,
        repo_auth_type: str=RepoAuthType.PUBLIC.name,
        hook_type: str= ProjectHookType.NONE.name,
        hook_data: dict=None,
        **kwargs) -> Project:
    """Adds a project to the database

    If the project has a RepoAuth that needs to be saved, the contents are encoded before saving them

    :param repo: (str) Id of the project
    :param session: (Session) Database session
    :param repo_auth_type: (str, optional) Repo authentication type
    :param hook_type: (ProjectHookType, optional) Project notification hook type
    :param hook_data: (str, optional) Project notification hook data

    :rtype: Project
    :raises sqlalchemy.exc.IntegrityError: On duplicated repo
    :raises AssertionError: On missing repo
    """
    assert type(repo) is str
    assert type(repo_auth_type) is str
    assert type(hook_type) is str

    # Check and build repo auth
    try:
        RepoAuthType[repo_auth_type]
    except KeyError:
        raise AssertionError('invalid repo auth type')

    repo_auth = {'repo_auth_type': repo_auth_type}

    # Check and build notification hooks
    try:
        ProjectHookType[hook_type]
    except KeyError:
        raise AssertionError('invalid hook type')

    hooks = {'hook_type': hook_type}
    if hook_type == ProjectHookType.SLACK.name:
        assert type(hook_data) is dict
        assert 'webhook_url' in hook_data
        hooks['hook_data'] = json.dumps(hook_data)

    # build the project object to persist in session
    project = Project(
        repo=repo,
        **repo_auth,
        **hooks
    )

    log.debug('save project {}'.format(project.to_dict()))

    session.add(project)
    return project


def delete_project(project_id: str, session: Session):
    """Delete a project from its id

    :param project_id: (str) Id of the project
    :param session: (Session) Database session
    """
    session.query(Project).filter(Project.id == project_id).delete()
    return


def delete_projects(session: Session):
    """Delete all projects

    :param session: (Session) Database session

    :rtype: No content
    """
    session.query(Project).delete()
    return


def get_project_by_repo(repo: str, session: Session) -> Project:
    """Get a project from its repo url

    :param repo: (str) repo of the project
    :param session: (Session) Database session

    :rtype: Project
    :raises ValueError: On invalid project_id or in not found Project
    """
    if repo is None:
        raise ValueError('Invalid project repo')

    project = session.query(Project).filter(Project.repo == repo).first()
    if project is None:
        raise ValueError('Project with repo {} not found in database'.format(repo))

    return project


def get_project(project_id: str, session: Session) -> Project:
    """Get a project from its id

    :param project_id: (str) Id of the project
    :param session: (Session) Database session

    :rtype: Project
    :raises ValueError: On invalid project_id or in not found Project
    """
    if project_id is None:
        raise ValueError('Invalid project id {}'.format(project_id))

    project = session.query(Project).get(project_id)
    if project is None:
        raise ValueError('Project {} not found in database'.format(project_id))

    return project


def get_projects(session: Session) -> Project:
    """Get all projects

    :param session: (Session) Database session

    :rtype: Project Array
    """

    projects = session.query(Project).all()
    if projects is None:
        return []

    return projects


def update_project(
        id: str, session: Session,
        repo_auth_type: str=None,
        hook_type: str=None,
        hook_data: str=None,
        **kwargs) -> Project:
    """Update a project data on the database

    If the project has a RepoAuth that needs to be saved, the contents are encoded before saving them

    :param id: (str) Id of the project
    :param session: (Session) Database session
    :param repo_auth_type: (str, optional) Project repository auth type
    :param hook_type: (str, optional) Project notification hook type
    :param hook_data: (str, optional) Project notification hook data

    :rtype: Project
    """

    update_dict = {}
    # checks valid auth type
    if repo_auth_type is not None:
        assert type(repo_auth_type) is str

        try:
            RepoAuthType[repo_auth_type]
        except KeyError:
            raise AssertionError('invalid repo auth type')

        update_dict['repo_auth_type'] = repo_auth_type

    # checks valid hook type
    if hook_type is not None:
        assert type(hook_type) is str

        try:
            ProjectHookType[hook_type]
        except KeyError:
            raise AssertionError('invalid hook type')

        update_dict['hook_type'] = hook_type

    if hook_data is not None:
        assert type(hook_data) is dict
        assert 'webhook_url' in hook_data
        update_dict['hook_data'] = json.dumps(hook_data)

    session.query(Project).filter(Project.id == id).update(update_dict)
    return get_project(id, session)


__all__ = ('add_project', 'delete_project', 'delete_projects', 'get_project', 'get_projects', 'update_project')
