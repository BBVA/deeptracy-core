import enum


class PluginSeverityEnum(enum.Enum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    NONE = 4


class PluginResult:

    def __init__(self,
                 library: str,
                 version: str,
                 severity: PluginSeverityEnum,
                 *,
                 summary: str = None,
                 advisory: str = None):
        """
        >>> PluginResult("retirejs", "1.0.1", PluginSeverityEnum.MEDIUM)

        :param library: Library name
        :param version: Version of library. i.e: 1.0.1 | 1.0.3-r5 ....
        :param severity: Severity level as a SeverityEnum enum
        :param summary: description of vulnerability
        :param advisory: associated CVE or similar unique identification
        """
        assert type(library) is str
        assert type(version) is str
        assert type(severity) is PluginSeverityEnum

        if summary is not None:
            assert type(summary) is str
        if advisory is not None:
            assert type(advisory) is str

        self.library = library
        self.version = version
        self.severity = severity.value
        self.summary = summary or ""
        self.advisory = advisory or ""


__all__ = ("PluginSeverityEnum", "PluginResult")
