from pytest import importorskip


def test_simple():
    importorskip("tests.assets.simple.main")
