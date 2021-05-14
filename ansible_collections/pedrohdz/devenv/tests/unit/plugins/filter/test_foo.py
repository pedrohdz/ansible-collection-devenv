from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
from plugins.filter.normalize_pyvenv_apps import convert_string


def test_convert_string():
    assert convert_string('foo') == {'name': 'foo'}


def test_foo():
    assert True
