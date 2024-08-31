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

def test_env_works():
    def uses_rich():
        from rich import print

        print("hello")
    
    Env("rich", python="3.12").run(uses_rich)
