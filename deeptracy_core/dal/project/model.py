# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from deeptracy_core.utils import make_uuid
from deeptracy_core.dal.database import Base
from deeptracy_core.dal.project.repo_auth import RepoAuthType


class Project(Base):
    """SQLAlchemy Project model"""
    __tablename__ = 'project'

    id = Column(String, primary_key=True, default=make_uuid)
    repo = Column(String, unique=True, nullable=False)
    repo_auth_type = Column(String, default=RepoAuthType.PUBLIC.name)
    repo_auth = Column(String)  # Auth is saved as a base64 string that represents a RepoAuth object

    scans = relationship('Scan')

    def to_dict(self):
        return {
            'id': self.id,
            'repo': self.repo,
            'scans': len(self.scans)
        }
