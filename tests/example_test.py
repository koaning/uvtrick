from pytest import importorskip


def test_demo():
    importorskip("examples.demo")

def test_simple():
    importorskip("examples.simple.main")
