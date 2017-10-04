# -*- coding: utf-8 -*-

from enum import Enum
from typing import List
from sqlalchemy.orm import Session
from deeptracy_core.dal.models import ScanAnalysisVulnerability
from deeptracy_core.dal.scan_analysis.model import ScanAnalysis
from deeptracy_core.dal.plugin_results import PluginResult


class ScanAnalysisState(Enum):
    PENDING = 'PENDING'


def get_scan_analysis(scan_analysis_id: str, session: Session) -> ScanAnalysis:
    scan_analysis = session.query(ScanAnalysis).get(scan_analysis_id)
    return scan_analysis


def add_scan_vulnerabilities_results(scan_analysis_id: str, vulnerabilities: List[PluginResult], session: Session):

    assert type(scan_analysis_id) is str

    for plugin_result in vulnerabilities:
        scan_analaysis_vul = ScanAnalysisVulnerability(
                                scan_analysis_id=scan_analysis_id,
                                library=plugin_result.library,
                                version=plugin_result.version,
                                severity=plugin_result.severity,
                                summary=plugin_result.summary,
                                advisory=plugin_result.advisory)
        session.add(scan_analaysis_vul)


def add_scan_analysis(scan_id: str, plugin_id: str, session: Session) -> ScanAnalysis:

    if scan_id is None:
        raise ValueError('Invalid scan id {}'.format(scan_id))

    if plugin_id is None:
        raise ValueError('Invalid plugin_id id {}'.format(plugin_id))

    scan_analysis = ScanAnalysis(scan_id=scan_id, plugin_id=plugin_id, state=ScanAnalysisState.PENDING.name)
    session.add(scan_analysis)
    return scan_analysis
