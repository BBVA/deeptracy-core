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

"""Manager function to deal with Vulnerability model"""

import logging

from sqlalchemy.orm import Session

from deeptracy_core.dal.scan_vul.model import ScanVulnerability
from deeptracy_core.dal.vulnerability.manager import get_or_create_vuln, get_or_create_vuln_in_scan

log = logging.getLogger(__name__)


def add_scan_vuln(scan_dep_id: str, scan_id: str, lang: str, cpe: str, cves: list, session: Session) \
        -> ScanVulnerability:
    """
    Add new dep to a scan

    :param scan_dep_id: (str) scan dependency id to associate the vulnerability scan
    :param scan_id: (str) scan id to associate the vulnerability scan
    :param lang: (str) Language of the scan
    :param cpe: (str) CPE that describe the vulnerability scan
    :param cves: (list) cves list for the current cpe
    :param session: (Session) database session to add objects
    :return:
    """
    assert type(scan_dep_id) is str
    assert type(scan_id) is str
    assert type(lang) is str
    assert type(cpe) is str
    assert type(cves) is list

    max_score = max([cve['score'] for cve in cves])

    vulnerabilities = [get_or_create_vuln(cpe, cve['cve'], session) for cve in cves]

    scan_vul = ScanVulnerability(scan_id=scan_id, lang=lang, cpe=cpe, max_score=max_score, scan_dep_id=scan_dep_id)
    session.add(scan_vul)
    session.commit()

    [
        get_or_create_vuln_in_scan(vulnerability_id=vulnerability.id, scan_dep_id=scan_dep_id, session=session)
        for vulnerability
        in vulnerabilities
    ]

    return scan_vul
