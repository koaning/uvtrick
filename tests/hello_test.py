from pytest import importorskip


def test_hello():
    importorskip("tests.assets.hello")
