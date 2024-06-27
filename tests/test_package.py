from __future__ import annotations

import importlib.metadata

import f2py_cmake as m


def test_version():
    assert importlib.metadata.version("f2py_cmake") == m.__version__
