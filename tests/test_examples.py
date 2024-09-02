from pathlib import Path

test_assets_dir = Path(__file__).parent

def test_add():
    from uvtrick import load

    script = test_assets_dir / "rich-script.py"
    add = load(script, "add")

    print(f"{add(1, 2)=}")
    print(f"{add(a=1, b=2)=}")


def test_hello():
    from uvtrick import load

    script = test_assets_dir / "rich-script.py"
    hello = load(script, "hello")
    print(f"{hello()=}")


def test_rich_versions():
    from uvtrick import Env

    rich_versions = (10, 11, 12, 13)
    print(f"Now iterating through {rich_versions=}:")


    def uses_rich(a, b):
        from importlib import metadata

        from rich import print

        version = metadata.version("rich")

        print(f"hello from rich=={version}")
        return a + b


    # This runs the function `uses_rich` in a new environment with the `rich` package installed.
    # Just like the `load` function, the result is returned via pickle.
    for version in rich_versions:
        result = Env(f"rich=={version}", python="3.12").run(uses_rich, a=1, b=2)
        print(f" --> add(1, 2) = {result}")


def test_simple():
    from uvtrick import load

    # Load the function `add` from the file `some_script.py`
    # It runs in another virtualenv, but you get back the response via pickle.
    # Be aware of the limitations, please only consider base Python objects.
    script = test_assets_dir / "some_script.py"
    add = load(script, "add")

    # This result is from the `some_script.py` file, running in another virtualenv
    # with `uv`. A pickle in a temporary file is used to communicate the result.
    result = add(1, 2)  # 3

    assert result == 3
    print(result)
