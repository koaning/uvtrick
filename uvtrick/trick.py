import subprocess
import pickle
from pathlib import Path
import tempfile
from textwrap import dedent
from collections.abc import Callable

__all__ = ("load", "uvtrick_")


def load(path: str | Path, func: Callable) -> Callable:
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


def uvtrick_(path: str | Path, func: Callable, *args, **kwargs):
    """This is a *very* hacky way to run functions from Python files from another virtual environment."""
    string_kwargs = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
    string_args = ", ".join([f"{a}" for a in args]) + ", " if args else ""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        script = temp_dir / "pytemp.py"
        output = temp_dir / "tmp.pickle"

        code = Path(path).read_text()
        idx = code.find("if __name__")
        code = code[:idx] + "\n\n"

        if func + "(" not in code:
            raise ValueError(f"Function {func} not found in the file {path}")
        if "# /// script" not in code:
            raise ValueError("Script metadata/dependencies not found in the file")

        main_template = dedent("""
        if __name__ == "__main__":
            import pickle
            with open('tmp.pickle', 'wb') as f:
                pickle.dump({func}({string_args} {string_kwargs}), f)
        """)

        code += main_template.format(
            func=func, string_args=string_args, string_kwargs=string_kwargs
        )
        script.write_text(code)
        # print(code)

        cmd = ["uv", "run", "--quiet", str(script)]
        subprocess.run(cmd, cwd=temp_dir, check=True)

        return pickle.loads(output.read_bytes())
