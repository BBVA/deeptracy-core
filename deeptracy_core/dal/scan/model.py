# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from deeptracy_core.utils import make_uuid
from deeptracy_core.dal.database import Base


class Scan(Base):
    """SQLAlchemy Scan model"""
    __tablename__ = 'scan'

    id = Column(String, primary_key=True, default=make_uuid)
    project_id = Column(String, ForeignKey('project.id'))
    lang = Column(String)
    analysis_count = Column(Integer, default=0)
    analysis_done = Column(Integer, default=0)
    state = Column(String, default='PENDING')
    source_path = Column(String)

    scan_analysis = relationship('ScanAnalysis', lazy='subquery')
    scan_vulnerabilities = relationship('ScanVulnerability', lazy='subquery')

    project = relationship('Project', lazy='subquery')

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'lang': self.lang,
            'analysis_count': self.analysis_count,
            'analysis_done': self.analysis_done,
            'state': self.state,
            'scan_analysis': self.scan_analysis
        }
