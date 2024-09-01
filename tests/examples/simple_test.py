from pytest import importorskip


def test_simple():
    importorskip("examples.simple.main")
