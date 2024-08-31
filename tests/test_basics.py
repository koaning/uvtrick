"""When I hacks this bad, I write tests."""

import pytest 
from uvtrick import load, Env

hello = load("tests/rich-script.py", "hello")
add = load("tests/rich-script.py", "add")


def test_smoke():
    assert hello() == 1


def test_args():
    assert add(1, 2) == 3
    assert add(a=1, b=4) == 5

def test_no_exist():
    with pytest.raises(ValueError):
        func = load("tests/rich-script.py", "no_exist")
        func()

def test_no_metadata():
    with pytest.raises(ValueError):
        func = load("tests/rich-fail.py", "add")
        func()

def test_env_works1():
    def uses_rich(a, b):
        from rich import print

        print("hello")
        return a + b

    for version in ["13", "12"]:
        assert Env(f"rich=={version}").run(uses_rich, a=1, b=2) == 3

def test_env_works2():
    def handles_all_types(arr, dictionary, string):
        return {"arr": arr, "dictionary": dictionary, "string": string}

    for version in ["13", "12"]:
        out = Env(f"rich=={version}").run(handles_all_types, arr=[1, 2, 3], dictionary={"a": 1, "b": 2}, string="hello") 
        assert out == {"arr": [1, 2, 3], "dictionary": {"a": 1, "b": 2}, "string": "hello"}
