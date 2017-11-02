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
    analysis_count = Column(Integer, default=0)
    analysis_done = Column(Integer, default=0)
    state = Column(String, default='PENDING')
    source_path = Column(String)
    created = Column(DateTime, default=datetime.now)

    scan_analysis = relationship('ScanAnalysis', lazy='subquery')
    scan_vulnerabilities = relationship('ScanVulnerability', lazy='subquery')

    project = relationship('Project', lazy='subquery')

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'lang': self.lang,
            'analysis_count': self.analysis_count,
            'analysis_done': self.analysis_done,
            'state': self.state,
            'scan_analysis': self.scan_analysis,
            'created': self.created
        }
