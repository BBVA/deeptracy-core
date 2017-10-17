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

import json

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from deeptracy_core.utils import make_uuid
from deeptracy_core.dal.database import Base
from deeptracy_core.dal.project.repo_auth import RepoAuthType
from deeptracy_core.dal.project.project_hooks import ProjectHookType


class Project(Base):
    """SQLAlchemy Project model"""
    __tablename__ = 'project'

    id = Column(String, primary_key=True, default=make_uuid)
    repo = Column(String, unique=True, nullable=False)
    repo_auth_type = Column(String, default=RepoAuthType.PUBLIC.name)
    repo_auth = Column(String, default='')  # Auth is saved as a base64 string that represents a RepoAuth object
    hook_type = Column(String, default=ProjectHookType.NONE.name)  # Notification hook type
    hook_data = Column(String, default='')  # Notification hook data

    scans = relationship('Scan')

    def to_dict(self):
        project = {
            'id': self.id,
            'repo': self.repo,
            'scans': len(self.scans),
            'hookType': self.hook_type,
            'authType': self.repo_auth_type
        }

        try:
            data_dict = json.loads(self.hook_data)
            project['hookData'] = data_dict
        except Exception:
            # if hook_data is not a valid json
            project['hookData'] = ''

        return project
