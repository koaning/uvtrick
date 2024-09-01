from pytest import importorskip, fmt_output
from inline_snapshot import snapshot


def test_rich_versions(capsys):
    importorskip("examples.rich_versions")
    captured = capsys.readouterr()
    assert fmt_output(captured.out) == snapshot(
        [
            "Now iterating through rich_versions=(10, 11, 12, 13):",
            " --> add(1, 2) = 3",
            " --> add(1, 2) = 3",
            " --> add(1, 2) = 3",
            " --> add(1, 2) = 3",
        ],
    )
    assert fmt_output(captured.err) == snapshot([])
