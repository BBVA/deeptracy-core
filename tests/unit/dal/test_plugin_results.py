import pytest

from deeptracy_core import PluginResult, PluginSeverityEnum


def test_plugin_result_ok():
    p = PluginResult("retire", "1.0.1", PluginSeverityEnum.MEDIUM)

    assert p.library == "retire"
    assert p.version == "1.0.1"
    assert p.severity == 2


def test_plugin_result_invalid_library_type():

    with pytest.raises(AssertionError):
        PluginResult(1, "1.0.1", PluginSeverityEnum.MEDIUM)


def test_plugin_result_invalid_version_type():

    with pytest.raises(AssertionError):
        PluginResult("retire", 1, PluginSeverityEnum.MEDIUM)


def test_plugin_result_invalid_serverity_type():

    with pytest.raises(AssertionError):
        PluginResult("retire", "1.0.1", "asdf")


def test_plugin_result_invalid_summary_type():

    with pytest.raises(AssertionError):
        PluginResult("retire",
                     "1.0.1",
                     PluginSeverityEnum.HIGH,
                     summary=1)


def test_plugin_result_invalid_advisory_type():

    with pytest.raises(AssertionError):
        PluginResult("retire",
                     "1.0.1",
                     PluginSeverityEnum.HIGH,
                     summary=1)
