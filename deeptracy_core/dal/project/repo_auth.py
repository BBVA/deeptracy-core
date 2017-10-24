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

"""Repo authorization

This classes are related to repository authorization inside a project

Attending to the RepoAuthType, repositories can be:
    RepoAuthType.PUBLIC: a public repository doesn't need authorization to pull
    RepoAuthType.LOCAL_PRIVATE_KEY: private key repository needs a private key to be able to pull code, and the private
        key is located in the host machine
    RepoAuthType.USER_PWD: the repo needs a user and password to authenticate to be able to pull

RepoAuth holds auth information for specific RepoAuthType. Object of type RepoAuth are intende
"""

import enum


class RepoAuthType(enum.Enum):
    PUBLIC = 'PUBLIC'
    LOCAL_PRIVATE_KEY = 'LOCAL_PRIVATE_KEY'
    # USER_PWD = 'USER_PWD'


class RepoAuth:
    def __init__(self, user_pwd: str=None):
        self.user_pwd = user_pwd

    def to_dict(self) -> dict:
        _dict = {}

        if self.user_pwd is not None:
            _dict['user_pwd'] = self.user_pwd

        return _dict
