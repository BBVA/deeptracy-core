# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, ForeignKey

from deeptracy_core.utils import make_uuid
from deeptracy_core.dal.database import Base


class ScanAnalysisVulnerability(Base):
    """SQLAlchemy ScanAnalysisVulnerability model"""
    __tablename__ = 'scan_analysis_vulnerability'

    id = Column(String, primary_key=True, default=make_uuid)
    scan_analysis_id = Column(String, ForeignKey('scan_analysis.id'))
    library = Column(String)
    version = Column(String)
    severity = Column(String)
    summary = Column(String)
    advisory = Column(String)


class ScanVulnerability(Base):
    """SQLAlchemy ScanVulnerability model"""
    __tablename__ = 'scan_vulnerability'

    id = Column(String, primary_key=True, default=make_uuid)
    scan_id = Column(String, ForeignKey('scan.id'))
    library = Column(String)
    version = Column(String)
    severity = Column(String)
    summary = Column(String)
    advisory = Column(String)
