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

from typing import List
from sqlalchemy.orm import Session

from .model import ScanVulnerability


def get_scan_vulnerabilities(scan_id: str, session: Session) -> List[ScanVulnerability]:
    """
    Return all the vulnerabilities for a given scan

    :param scan_id:
    :param session:
    :return:
    """
    scan_vuls = session.query(ScanVulnerability).filter(ScanVulnerability.scan_id == scan_id).all()
    return scan_vuls


def add_scan_vulnerabilities(scan_id: str, vulnerabilities: List[dict], session: Session):
    """
    Bulk add vulnerabilities to a given scan

    :param scan_id:
    :param vulnerabilities:
    :param session:
    :return:
    """
    assert type(scan_id) is str

    for result in vulnerabilities:
        scan_vul = ScanVulnerability(
                                scan_id=scan_id,
                                library=result.get('library', None),
                                version=result.get('version', None),
                                severity=result.get('severity', None),
                                summary=result.get('summary', None),
                                advisory=result.get('advisory', None))
        session.add(scan_vul)
