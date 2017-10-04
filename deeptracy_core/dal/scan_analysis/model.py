# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from deeptracy_core.utils import make_uuid
from deeptracy_core.dal.database import Base


class ScanAnalysis(Base):
    """SQLAlchemy ScanAnalysis model"""
    __tablename__ = 'scan_analysis'

    id = Column(String, primary_key=True, default=make_uuid)
    scan_id = Column(String, ForeignKey('scan.id'))
    plugin_id = Column(String, ForeignKey('plugin.id'))
    state = Column(String)

    scan_analysis_vulnerability = relationship('ScanAnalysisVulnerability')
    plugin = relationship('Plugin')
    scan = relationship('Scan', lazy='subquery')
