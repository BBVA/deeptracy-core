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
