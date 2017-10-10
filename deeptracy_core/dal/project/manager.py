# -*- coding: utf-8 -*-
"""Manager function to deal with Project model"""
import base64
import pickle

from sqlalchemy.orm import Session
from deeptracy_core.dal.project.model import Project
from deeptracy_core.dal.project.repo_auth import RepoAuthType, RepoAuth


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
        hook_type: str=None,
        hook_data: str=None,
        **kwargs) -> Project:
    """Update a project data on the database

    If the project has a RepoAuth that needs to be saved, the contents are encoded before saving them

    :param id: (str) Id of the project
    :param session: (Session) Database session
    :param hook_type: (str, optional) Project notification hook type
    :param hook_data: (str, optional) Project notification hook data

    :rtype: Project
    """

    update_dict = {}
    if hook_type is not None:
        assert type(hook_type) is str
        update_dict['hook_type'] = hook_type

    if hook_data is not None:
        assert type(hook_data) is str
        update_dict['hook_data'] = hook_data

    session.query(Project).filter(Project.id == id).update(update_dict)
    return get_project(id, session)


__all__ = ('add_project', 'delete_project', 'delete_projects', 'get_project', 'get_projects', 'update_project')
