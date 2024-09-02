from pytest import importorskip, fmt_output
from inline_snapshot import snapshot


def test_simple(capsys):
    importorskip("examples.simple.main")
    captured = capsys.readouterr()
    assert fmt_output(captured.out) == snapshot(
        ["3"],
    )
    assert fmt_output(captured.err) == snapshot(
        [
            (
                "file='some_script.py', func='add'",
                """\
```
# /// script
# dependencies = [
# ]
# ///


def add(a: int, b: int):
    return a + b

if __name__ == "__main__":
    import pickle
    with open('tmp.pickle', 'wb') as f:
        pickle.dump(add(1, 2,  ), f)
```\
""",
            )
        ],
    )
