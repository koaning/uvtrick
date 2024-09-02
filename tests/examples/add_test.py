from pytest import importorskip, fmt_output
from inline_snapshot import snapshot


def test_add(capsys):
    importorskip("examples.add")
    captured = capsys.readouterr()
    assert fmt_output(captured.out) == snapshot(
        ["add(1, 2)=3", "add(a=1, b=2)=3"],
    )
    assert fmt_output(captured.err) == snapshot(
        [
            (
                "file='rich_script.py', func='add'",
                """\
```
# /// script
# dependencies = [
#   "rich",
# ]
# ///
import rich


def hello():
    rich.print("Hello, World!")
    return 1


def add(a, b):
    return a + b

if __name__ == "__main__":
    import pickle
    with open('tmp.pickle', 'wb') as f:
        pickle.dump(add(1, 2,  ), f)
```\
""",
            ),
            (
                "file='rich_script.py', func='add'",
                """\
```
# /// script
# dependencies = [
#   "rich",
# ]
# ///
import rich


def hello():
    rich.print("Hello, World!")
    return 1


def add(a, b):
    return a + b

if __name__ == "__main__":
    import pickle
    with open('tmp.pickle', 'wb') as f:
        pickle.dump(add( a=1, b=2), f)
```\
""",
            ),
        ],
    )
