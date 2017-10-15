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

import enum


class PluginSeverityEnum(enum.Enum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    NONE = 4


class PluginResult:

    __slots__ = ['library', 'version', 'severity', 'summary', 'advisory']

    def __init__(self,
                 library: str,
                 version: str,
                 severity: PluginSeverityEnum,
                 *,
                 summary: str = None,
                 advisory: str = None):
        """
        >>> PluginResult('retirejs', '1.0.1', PluginSeverityEnum.MEDIUM)

        :param library: Library name
        :param version: Version of library. i.e: 1.0.1 | 1.0.3-r5 ....
        :param severity: Severity level as a SeverityEnum enum
        :param summary: description of vulnerability
        :param advisory: associated CVE or similar unique identification
        """
        assert type(library) is str
        assert type(version) is str
        assert isinstance(severity, PluginSeverityEnum)

        if summary is not None:
            assert type(summary) is str
        if advisory is not None:
            assert type(advisory) is str

        self.library = library
        self.version = version
        self.severity = severity.value
        self.summary = summary or None
        self.advisory = advisory or None

    def to_dict(self):
        """
        Get a serializable dict from the object with all his slots

        :return: dictionary with all the attributes defined in the slots
        """
        return {slot: getattr(self, slot) for slot in self.__slots__}


__all__ = ('PluginSeverityEnum', 'PluginResult')
