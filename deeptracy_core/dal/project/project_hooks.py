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

"""Project Notification Hooks

This classes are related to project notifications
"""

import enum


class ProjectHookType(enum.Enum):
    NONE = 'NONE'
    SLACK = 'SLACK'


class ProjectHookData:
    def __init__(self, slack_data: str=None):
        self.slack_data = slack_data

    def to_dict(self) -> dict:
        _dict = {}

        if self.user_pwd is not None:
            _dict['user_pwd'] = self.user_pwd

        return _dict
