"""Repo authorization

This classes are related to repository authorization inside a project

Attending to the RepoAuthType, repositories can be:
    RepoAuthType.PUBLIC: a public repository doesn't need authorization to pull
    RepoAuthType.PRIVATE_KEY: private key repository needs a private key to be able to pull code

RepoAuth holds auth information for specific RepoAuthType. Object of type RepoAuth are intende
"""

import enum


class RepoAuthType(enum.Enum):
    PUBLIC = 'PUBLIC'
    PRIVATE_KEY = 'PRIVATE_KEY'


class RepoAuth:
    def __init__(self, pkey_str: str=None):
        self.pkey_str = pkey_str

    def to_dict(self) -> dict:
        _dict = {}

        if self.pkey_str is not None:
            _dict['pkey_str'] = self.pkey_str

        return _dict
