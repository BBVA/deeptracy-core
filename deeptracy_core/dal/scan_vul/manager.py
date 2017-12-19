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
from deeptracy_core.dal.models import Vulnerability

log = logging.getLogger(__name__)


def add_scan_vul(scan_id: str, library: str, version: str, vulnerabilities: list, session: Session) \
        -> ScanVulnerability:
    """
    Add new dep to a scan

    :param scan_id: (str) scan id to associate the vulnerability
    :param library: (str) package name
    :param version: (str) package version
    :param vulnerabilities: (list) Vulnerabilities list for the current scan
    :param session: (Session) database session to add objects
    :return:
    """
    assert type(scan_id) is str
    assert type(library) is str
    assert type(version) is str
    assert type(vulnerabilities) is list

    max_score = [0]

    scan_vul = ScanVulnerability(scan_id=scan_id, library=library, version=version)
    session.add(scan_vul)
    session.commit()

    def add_vulnerability(vulnerability):

        [cpe, cve, patton_id, ref_type, href, prod_title, score, access_vector, source] = vulnerability

        if score > max_score[0]:
            max_score[0] = score

        new_vulnerability = Vulnerability(scan_vulnerability_id=scan_vul.id, cpe=cpe, cve=cve,
                                          patton_id=patton_id, ref_type=ref_type, href=href,
                                          prod_title=prod_title, score=score, access_vector=access_vector,
                                          source=source)
        return new_vulnerability

    created_vulnerabilities = [add_vulnerability(vulnerability) for vulnerability in vulnerabilities]
    session.add_all(created_vulnerabilities)
    scan_vul.max_score = max_score[0]
    session.add(scan_vul)
    session.commit()
    return scan_vul
