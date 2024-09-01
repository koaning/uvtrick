from pytest import importorskip


def test_hello():
    importorskip("examples.hello")
