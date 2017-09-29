# -*- coding: utf-8 -*-
"""Manager function to deal with Project model"""

from sqlalchemy.orm import Session
from deeptracy_core.dal.project.model import Project


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


def add_project(repo: str, session: Session) -> Project:
    """Adds a project to the database

    :param repo: (str) Id of the project
    :param session: (Session) Database session

    :rtype: Project
    :raises sqlalchemy.exc.IntegrityError: On duplicated repo
    :raises AssertionError: On missing repo
    """
    assert type(repo) is str

    project = Project(repo=repo)
    session.add(project)
    return project


__all__ = ('get_project', 'add_project')
