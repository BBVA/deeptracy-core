# -*- coding: utf-8 -*-

from enum import Enum
from sqlalchemy.orm import Session
from deeptracy_core.dal.scan.model import Scan


class ScanState(Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    INVALID_REPO = 'INVALID_REPO'
    NO_PLUGINS_FOR_LANGUAJE = 'NO_PLUGINS_FOR_LANGUAJE'


def add_scan(project_id: str, lang: str, session: Session) -> Scan:
    """Adds a scan related to a project"""
    assert type(project_id) is str
    assert type(lang) is str

    scan = Scan(project_id=project_id, lang=lang)
    session.add(scan)
    return scan


def get_scan(scan_id: str, session: Session) -> Scan:
    """Get a project from its id"""
    assert type(scan_id) is str

    scan = session.query(Scan).get(scan_id)
    return scan


def update_scan_state(scan: Scan, state: ScanState, session: Session) -> Scan:
    if scan.id is None:
        raise ValueError('Cant create scans')

    scan.state = state.name
    session.add(scan)
    return scan


__all__ = ('ScanState', 'add_scan', 'get_scan', 'update_scan_state')
