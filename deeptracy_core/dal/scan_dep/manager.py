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

"""Manager function to deal with Scan Dependencies model"""

import logging

from datetime import datetime
from sqlalchemy.orm import Session
from deeptracy_core.dal.scan_dep.model import ScanDep

log = logging.getLogger(__name__)


def add_scan_dep(scan_id: str, dep: str, found_at: datetime, session: Session) -> ScanDep:
    """
    Add new dep to a scan

    :param scan_id: (str) scan id to asociate the dependency
    :param dep: (str) raw dependency description
    :param found_at: (datetime) dependency datetime when it was found. This filed is used to group up dependencies
    :param session: (Session) database session to add objects
    :return:
    """
    assert type(scan_id) is str
    assert type(dep) is str
    assert type(found_at) is datetime

    scan_dep = ScanDep(scan_id=scan_id, raw_dep=dep, found_at=found_at)
    session.add(scan_dep)
    return scan_dep


def add_scan_deps(scan_id: str, deps: list, found_at: datetime, session: Session) -> ScanDep:
    """
    Add new deps in bulk to a scan

    :param scan_id: (str) scan id to asociate the dependency
    :param deps: (list) list of raw dependency description
    :param found_at: (datetime) dependency datetime when it was found. This filed is used to group up dependencies
    :param session: (Session) database session to add objects
    :return:
    """
    assert type(scan_id) is str
    assert type(deps) is list and len(deps) > 0
    assert type(found_at) is datetime

    dep_list = []
    for dep in deps:
        scan_dep = ScanDep(scan_id=scan_id, raw_dep=dep, found_at=found_at)
        dep_list.append(scan_dep)

    session.add_all(dep_list)
    return dep_list


def compare_scan_deps(scan_id: str, compare_scan_id: str, session: Session) -> bool:
    """
    Given two scans id, compare the dependecies for both and return True if they have
    the same dependencies and False if they don't

    :param scan_id: (str) scan id to check
    :param compare_scan_id: (str) another scan id to check
    :param session: (Session) database session to add objects
    :return: (bool) True if deps are indentical, else return false
    """
    assert type(scan_id) is str
    assert type(compare_scan_id) is str

    deps_scan_1 = session.query(ScanDep).filter(ScanDep.scan_id == scan_id).all()
    deps_scan_2 = session.query(ScanDep).filter(ScanDep.scan_id == compare_scan_id).all()

    raw_deps_1 = [scan_dep.raw_dep for scan_dep in deps_scan_1]
    raw_deps_2 = [scan_dep.raw_dep for scan_dep in deps_scan_2]

    diff = list(set(raw_deps_1).symmetric_difference(set(raw_deps_2)))
    return len(diff) == 0


__all__ = ('add_scan_dep', 'add_scan_deps', 'compare_scan_deps')
