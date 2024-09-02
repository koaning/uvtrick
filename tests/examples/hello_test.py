from pytest import importorskip, fmt_output
from inline_snapshot import snapshot


def test_hello(capsys):
    importorskip("examples.hello")
    captured = capsys.readouterr()
    assert fmt_output(captured.out) == snapshot(["hello()=1"])
    assert fmt_output(captured.err) == snapshot(
        [
            (
                "file='rich_script.py', func='hello'",
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
        pickle.dump(hello( ), f)
```\
""",
            )
        ],
    )
