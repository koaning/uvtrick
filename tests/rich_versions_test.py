from pytest import importorskip


def test_rich_versions():
    importorskip("tests.assets.rich_versions")
