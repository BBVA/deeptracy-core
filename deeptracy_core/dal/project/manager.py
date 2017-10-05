# -*- coding: utf-8 -*-
"""Manager function to deal with Project model"""
import base64
import pickle

from sqlalchemy.orm import Session
from deeptracy_core.dal.project.model import Project
from deeptracy_core.dal.project.repo_auth import RepoAuthType, RepoAuth


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


def add_project(
        repo: str, session: Session,
        repo_auth_type: RepoAuthType=RepoAuthType.PUBLIC,
        repo_auth: RepoAuth=None) -> Project:
    """Adds a project to the database

    If the project has a RepoAuth that needs to be saved, the contents are encoded before saving them

    :param repo: (str) Id of the project
    :param session: (Session) Database session
    :param repo_auth_type: (RepoAuthType, optional, default RepoAuthType.PUBLIC) Repo authentication type
    :param repo_auth: (ProjectAuth, optional) Project auth data if project is not public

    :rtype: Project
    :raises sqlalchemy.exc.IntegrityError: On duplicated repo
    :raises AssertionError: On missing repo
    """
    assert type(repo) is str
    assert type(repo_auth_type) is RepoAuthType

    encoded_auth = None
    if repo_auth_type is RepoAuthType.USER_PWD:
        assert type(repo_auth) is RepoAuth
        assert type(repo_auth.user_pwd) is str

        pickled = pickle.dumps(repo_auth.to_dict())
        encoded_auth = base64.b64encode(pickled)

    project = Project(repo=repo, repo_auth_type=repo_auth_type.name, repo_auth=encoded_auth)
    session.add(project)
    return project


__all__ = ('get_project', 'add_project')
