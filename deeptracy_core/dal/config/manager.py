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

from sqlalchemy.orm import Session
from .model import Config


def save_config(key: str, value: str, session: Session) -> Config:
    """Save or update a configuration"""
    assert type(key) is str
    assert type(value) is str

    config = session.query(Config).get(key)
    if not config:
        config = Config(id=key, value=value)
    else:
        config.value = value

    session.add(config)

    return config


def get_config(key: str, session: Session) -> Config:
    """retrieve a configuration"""
    assert type(key) is str

    config = session.query(Config).get(key)

    return None if not config else config.value


__all__ = ('save_config', 'get_config')
