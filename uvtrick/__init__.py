from __future__ import annotations

import inspect
import cloudpickle
import subprocess
import tempfile
import textwrap
from collections.abc import Callable
from pathlib import Path
import warnings


def argskwargs_to_callstring(func, *args, **kwargs) -> str:
    string_kwargs = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
    string_args = ", ".join([f"{a}" for a in args]) + ", " if args else ""
    return f"{func.__name__}({string_args} {string_kwargs})"


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

        code += f"""if __name__ == "__main__":
    import cloudpickle
    with open('tmp.pickle', 'wb') as f:
        cloudpickle.dump({func}({string_args} {string_kwargs}), f)\n"""

        script.write_text(code)
        # print(code)
        cmd = ["uv", "run", "--with=cloudpickle", "--quiet", str(script)]
        subprocess.run(cmd, cwd=temp_dir, check=True)

        return cloudpickle.loads(output.read_bytes())


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
    # It runs in another virtualenv, but you get back the response via cloudpickle. 
    # Be aware of the limitations, please only consider base Python objects.
    hello = load("some_script.py", "hello")
    ```
    """
    def load_func(*args, **kwargs):
        return uvtrick_(path, func, *args, **kwargs)
    return load_func


class Env:
    """
    Represents a virtual environment with a specific Python version and set of dependencies.
    
    Args:
        *requirements: A list of dependencies to install in the virtual environment.
        python (str): The Python version to use in the virtual environment.
        debug (bool): If True, the script contents will be printed to STDOUT.
        temp_dir (Path): The temporary directory where the script and pickled inputs/outputs are stored.
        env (dict): A dictionary of environment variables to set when running the script.
    """
    def __init__(self, *requirements: str, python: str = None, debug: bool = False, env: dict[str, str] | None = None):
        self.requirements = requirements
        self.python = python
        self.debug = debug
        self.temp_dir: Path = None
        self.env = env

    @property
    def inputs(self) -> Path:
        return self.temp_dir / "pickled_inputs.pickle"

    @property
    def script(self) -> Path:
        return self.temp_dir / "pytemp.py"

    @property
    def output(self) -> Path:
        return self.temp_dir / "tmp.pickle"

    @property
    def cmd(self) -> list[str]:
        quiet = [] if self.debug else ["--quiet"]
        deps = [f"--with={dep}" for dep in self.requirements]
        pyversion = [f"--python={self.python}"] if self.python else []
        return ["uv", "run","--with=cloudpickle", *quiet, *deps, *pyversion, str(self.script)]

    def report(self, contents: str) -> None:
        """Log the temporary dir, input kw/args and intermediate script to STDOUT."""
        print(f"Running files in {self.temp_dir}\n{self.cmd}")
        args, kwargs = cloudpickle.loads(self.inputs)
        print(f"Pickled args: {args}")
        print(f"Pickled kwargs: {kwargs}")
        print(f"Contents of the script:\n\n{contents}")
        return

    def maincall(self, func: Callable) -> str:
        """A main block to deserialise a function signature then serialise a result.

        Load the args/kwargs from an 'inputs' cloudpickle, call a Python function
        with them, and store the result in an 'output' cloudpickle.
        """
        func_name = func.__name__
        inputs_path, output_path = self.inputs, self.output
        return textwrap.dedent(f"""
        if __name__ == "__main__":
            import cloudpickle
            from pathlib import Path
            import os
            
            args, kwargs, environment_variables = cloudpickle.loads(Path('{inputs_path!s}').read_bytes())
            if environment_variables:
                os.environ.update(environment_variables)

            result = {func_name}(*args, **kwargs)
            Path('{output_path!s}').write_bytes(cloudpickle.dumps(result))
        """)

    def run(self, func: Callable, *args, **kwargs):
        """Run a function in the virtual environment using uv."""
        with tempfile.TemporaryDirectory() as temp_dir:
            self.temp_dir = Path(temp_dir)
            # First pickle the inputs and environment variables
            self.inputs.write_bytes(cloudpickle.dumps((args, kwargs, self.env)))
            # Now write the contents of the script
            func_source = textwrap.dedent(inspect.getsource(func))
            contents = func_source + "\n\n" + self.maincall(func)
            self.script.write_text(contents)

            if self.debug:
                self.report(contents)
            subprocess.run(self.cmd, cwd=temp_dir, check=True)
            # Lastly load the stored result of running the script
            return cloudpickle.loads(self.output.read_bytes())
