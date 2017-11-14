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

from datetime import datetime, timedelta
from enum import Enum
from sqlalchemy.orm import Session
from deeptracy_core.dal.scan.model import Scan


class ScanState(Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    DONE = 'DONE'
    INVALID_REPO = 'INVALID_REPO'
    NO_PLUGINS_FOR_LANGUAGE = 'NO_PLUGINS_FOR_LANGUAGE'
    INVALID_YML_ON_PROJECT = 'INVALID_YML_ON_PROJECT'
    CANT_GET_LANGUAGE = 'CANT_GET_LANGUAGE'
    SAME_DEPS_AS_PREVIOUS = 'SAME_DEPS_AS_PREVIOUS'


def add_scan(project_id: str, session: Session, lang=None) -> Scan:
    """Adds a scan related to a project"""
    assert type(project_id) is str

    scan = Scan(project_id=project_id, lang=lang)
    session.add(scan)
    return scan


def get_scan(scan_id: str, session: Session) -> Scan:
    """Get a project from its id"""
    assert type(scan_id) is str

    scan = session.query(Scan).get(scan_id)
    return scan


def update_scan_state(scan: Scan, state: ScanState, session: Session) -> Scan:
    """Updates a scan state"""
    if scan.id is None:
        raise ValueError('Cant create scans')

    scan.state = state.name
    session.add(scan)
    return scan


def get_previous_scan_for_project(project_id: str, scan_id: str, session: Session) -> bool:
    """
    Given a project and a scan id, return a the previous scan for the project

    :param project_id:
    :param scan_id:
    :param session:
    :return:
    """
    scan = get_scan(scan_id, session)

    previous_scan = session.query(Scan) \
        .filter(Scan.project_id == project_id) \
        .filter(Scan.created < scan.created) \
        .order_by(Scan.created.desc()) \
        .first()

    return previous_scan


def get_num_scans_in_last_minutes(project_id: str, minutes: int, session: Session) -> int:
    """
    Return the number of scans ran in the last N minutes for a project

    :param project_id:
    :param minutes:
    :param session:
    :return:
    """

    assert type(project_id) is str
    assert type(minutes) is int

    from_time = datetime.now() - timedelta(minutes=minutes)
    number = session.query(Scan) \
        .filter(Scan.created > from_time) \
        .filter(Scan.project_id == project_id) \
        .count()

    return number


__all__ = ('ScanState', 'add_scan', 'get_scan', 'update_scan_state', 'get_previous_scan_for_project')
