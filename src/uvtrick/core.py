from collections.abc import Callable
from .trick import uvtrick_

__all__ = ("maincall", "load")


def maincall(func: Callable, inputs_path: str, outputs_path: str) -> str:
    func_name = func.__name__
    return f"""
if __name__ == "__main__":
    import pickle
    from pathlib import Path

    args, kwargs = pickle.loads(Path(inputs_path).read_bytes())
    result = {func_name}(*args, **kwargs)
    Path(outputs_path).write_bytes(pickle.dumps(result))
"""


def load(path, func):
    """
    Load a function from a Python file, this function will be executed in a separate virtual environment using uv.

    Note that this approach is more of a demo, it is very hacky and it assumes that the Python script in question
    uses inline script metadata. More information on this feature can be found here:

    - https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies
    - https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata

    Usage:

    ```python
    from uvtrick import load

    # Load the function `hello` from the file `some_script.py`
    # It runs in another virtualenv, but you get back the response via pickle.
    # Be aware of the limitations, please only consider base Python objects.
    hello = load("some_script.py", "hello")
    ```
    """

    def load_func(*args, **kwargs):
        return uvtrick_(path, func, *args, **kwargs)

    return load_func
