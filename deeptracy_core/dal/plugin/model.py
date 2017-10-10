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

from sqlalchemy import Column, String, Boolean

from deeptracy_core.utils import make_uuid
from deeptracy_core.dal.database import Base


class Plugin(Base):
    """SQLAlchemy Plugin model"""
    __tablename__ = 'plugin'

    id = Column(String, primary_key=True, default=make_uuid)
    name = Column(String)
    lang = Column(String)
    active = Column(Boolean)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'lang': self.lang,
            'active': self.active
        }
