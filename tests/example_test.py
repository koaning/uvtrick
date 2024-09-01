from pytest import importorskip
from inline_snapshot import snapshot


def test_hello(capsys):
    importorskip("examples.hello")
    assert capsys.readouterr().out == snapshot(
        """\
hello()=1
"""
    )


def test_add(capsys):
    importorskip("examples.add")
    assert capsys.readouterr().out == snapshot(
        """\
add(1, 2)=3
add(a=1, b=2)=3
"""
    )


def test_rich_versions(capsys):
    importorskip("examples.rich_versions")
    assert capsys.readouterr().out == snapshot(
        """\
Now iterating through rich_versions=(10, 11, 12, 13):
 --> add(1, 2) = 3
 --> add(1, 2) = 3
 --> add(1, 2) = 3
 --> add(1, 2) = 3
"""
    )


def test_simple(capsys):
    importorskip("examples.simple.main")
    assert capsys.readouterr().out == snapshot(
        """\
3
"""
    )
