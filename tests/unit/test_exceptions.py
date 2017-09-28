# -*- coding: utf-8 -*-
"""tests for DeeptracyException class"""

import pytest

from deeptracy_core.exceptions import DeeptracyException


def test_deeptracy_exception_holds_an_api_status_code():
    """Deeptracy exception class should holds an attribute
    to save the api status code to return in case of that exception"""
    status_code = 201
    with pytest.raises(DeeptracyException) as excinfo:
        raise DeeptracyException('custom message', status_code=status_code)

    assert excinfo.value.status_code == status_code


def test_deeptracy_exception_holds_an_api_status_code():
    """Deeptracy exception class should holds a message"""
    msg = 'custom message'
    with pytest.raises(DeeptracyException) as excinfo:
        raise DeeptracyException(msg)

    assert msg in str(excinfo.value)
