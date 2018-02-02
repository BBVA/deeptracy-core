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


def add_scan_deps(scan_id: str, scan_deps: list, found_at: datetime, session: Session) -> ScanDep:
    """
    Add new deps in bulk to a scan

    :param scan_id: (str) scan id to asociate the dependency
    :param scan_deps: (list) list of [library, version] that identify a library
    :param found_at: (datetime) dependency datetime when it was found. This filed is used to group up dependencies
    :param session: (Session) database session to add objects
    :return:
    """
    assert type(scan_id) is str
    assert type(scan_deps) is list and len(scan_deps) > 0
    assert type(found_at) is datetime
    scan_deps_list = [ScanDep(scan_id=scan_id, library=scan_dep[0], version=scan_dep[1],
                              raw_dep='{}:{}'.format(scan_dep[0], scan_dep[1]), found_at=found_at)
                      for scan_dep in scan_deps]
    session.add_all(scan_deps_list)
    return scan_deps_list


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


def get_scan_dep_by_id(id: str, session: Session) -> ScanDep:
    """
    Given a scan dep id, return the dependencies for the scan

    :param id: (str) scan dep id to check
    :param session: (Session) database session to add objects

    :rtype: ScanDep
    :raises ValueError: On invalid id or in not found Scan Dep
    """
    return session.query(ScanDep).filter(ScanDep.id == id).one()


def get_scan_deps(scan_id: str, session: Session) -> ScanDep:
    """
    Given a scans id, return the dependencies for the scan

    :param scan_id: (str) scan id to check
    :param session: (Session) database session to add objects

    :rtype: ScanDep
    :raises ValueError: On invalid scan_id or in not found Scan Dep
    """
    return session.query(ScanDep).filter(ScanDep.scan_id == scan_id).all()


def get_scan_by_raw_dep(raw_dep: str, session: Session) -> ScanDep:
    """
    Given a raw dependencies, return the dependencies with this raw_dep

    :param raw_dep: (str) raw_dep to check
    :param session: (Session) database session to add objects

    :rtype: ScanDep
    :raises ValueError: On invalid raw_dep or in not found Scan Dep
    """
    return session.query(ScanDep).filter(ScanDep.raw_dep == raw_dep).all()


def get_scan_dep_by_scan_id_and_raw_dep(scan_id: str, raw_dep: str, session: Session) -> ScanDep:
    """
    Given a scan id and raw dependencies , return the dependency with this scan_id and raw_dep

    :param scan_id: (str) scan_id to check
    :param raw_dep: (str) raw_dep to check
    :param session: (Session) database session to add objects

    :rtype: ScanDep
    :raises ValueError: On invalid scan_id, raw_dep or in not found Scan Deps
    """
    return session.query(ScanDep).filter(ScanDep.scan_id == scan_id).filter(ScanDep.raw_dep == raw_dep).one()


__all__ = ('add_scan_dep', 'add_scan_deps', 'compare_scan_deps', 'get_scan_dep_by_id', 'get_scan_deps',
           'get_scan_by_raw_dep', 'get_scan_dep_by_scan_id_and_raw_dep')
