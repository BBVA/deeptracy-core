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

from sqlalchemy import Column, String, Float, ForeignKey, Sequence
from sqlalchemy.orm import relationship

from deeptracy_core.dal.database import Base

TABLE_ID = Sequence('table_id_seq', start=1)


class Vulnerability(Base):
    """SQLAlchemy ScanVulnerability model"""
    __tablename__ = 'vulnerability'

    id = Column(String, TABLE_ID, primary_key=True, server_default=TABLE_ID.next_value())
    scan_vulnerability_id = Column(String, ForeignKey('scan_vulnerability.id'))
    cpe = Column(String)
    cve = Column(String)
    patton_id = Column(String)
    ref_type = Column(String)
    href = Column(String)
    prod_title = Column(String)
    score = Column(Float)
    access_vector = Column(String)
    source = Column(String)

    scan_vulnerability = relationship('ScanVulnerability', lazy='subquery')

    def to_dict(self):
        return {
            'id': self.id,
            'cpe': self.cpe,
            'cve': self.cve,
            'patton_id': self.patton_id,
            'ref_type': self.ref_type,
            'href': self.href,
            'prod_title': self.prod_title,
            'score': self.score,
            'access_vector': self.access_vector,
            'source': self.source
        }
