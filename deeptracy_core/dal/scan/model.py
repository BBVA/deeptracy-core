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

from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from deeptracy_core.utils import make_uuid
from deeptracy_core.dal.database import Base


class Scan(Base):
    """SQLAlchemy Scan model"""
    __tablename__ = 'scan'

    id = Column(String, primary_key=True, default=make_uuid)
    project_id = Column(String, ForeignKey('project.id'))
    lang = Column(String)
    branch = Column(String, default='master')
    state = Column(String, default='PENDING')
    source_path = Column(String)
    created = Column(DateTime, default=datetime.now)
    total_packages = Column(Integer, default=0)
    total_vulnerabilities = Column(Integer, default=0)

    scan_dependencies = relationship('ScanDep')
    scan_vulnerabilities = relationship('ScanVulnerability')

    project = relationship('Project', lazy='subquery')

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'lang': self.lang,
            'branch': self.branch,
            'state': self.state,
            'created': self.created,
            'total_packages': self.total_packages,
            'total_vulnerabilities': self.total_vulnerabilities
        }
