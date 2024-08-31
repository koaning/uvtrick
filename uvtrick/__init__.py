import textwrap
import subprocess
import pickle
import inspect
from pathlib import Path
import tempfile
import os

PICKLED_INPUTS_PATH = "pickled_inputs.pickle"
PICKLED_OUTPUTS_PATH = "tmp.pickle"

def argskwargs_to_callstring(func, *args, **kwargs):
    string_kwargs = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
    string_args = ", ".join([f"{a}" for a in args]) + ", " if args else ""
    return f"{func.__name__}({string_args} {string_kwargs})"


def maincall(func, inputs_path, outputs_path):
    return f"""
if __name__ == "__main__":
    import pickle

    with open('{inputs_path}', 'rb') as file:
        args, kwargs = pickle.load(file)

    with open('{outputs_path}', 'wb') as f:
        pickle.dump({func.__name__}(*args, **kwargs), f)
"""

def uvtrick_(path, func, *args, **kwargs):
    """This is a *very* hacky way to run functions from Python files from another virtual environment."""
    string_kwargs = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
    string_args = ", ".join([f"{a}" for a in args]) + ", " if args else ""


    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        code = Path(path).read_text()
        idx = code.find("if __name__")
        code = code[:idx] + "\n\n"

        if func + "(" not in code:
            raise ValueError(f"Function {func} not found in the file {path}")
        if "# /// script" not in code:
            raise ValueError("Script metadata/dependencies not found in the file")

        code += f"""if __name__ == "__main__":
    import pickle
    with open('tmp.pickle', 'wb') as f:
        pickle.dump({func}({string_args} {string_kwargs}), f)\n"""

        Path(temp_dir / "pytemp.py").write_text(code)
        # print(code)
        subprocess.run(f"uv run --quiet {str(temp_dir / 'pytemp.py')}", shell=True, cwd=temp_dir)

        temp_pickle_path = os.path.join(temp_dir, "tmp.pickle")
        with open(temp_pickle_path, 'rb') as file:
            loaded_data = pickle.load(file)
    return loaded_data


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


class Env:
    """Represents a virtual environment with a specific Python version and set of dependencies."""
    def __init__(self, *requirements, python=None, debug=False):
        self.requirements = requirements
        self.python = python
        self.debug = debug

    def run(self, func, *args, **kwargs):
        """Run a function in the virtual environment using uv."""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Lets first pickle the inputs
            temp_dir = Path(temp_dir)
            with open(temp_dir / "pickled_inputs.pickle", "wb") as f:
                pickle.dump((args, kwargs), f)
            
            # Now write the contents of the script
            contents = textwrap.dedent(inspect.getsource(func))
            contents += "\n\n"
            contents += maincall(func, temp_dir / PICKLED_INPUTS_PATH, temp_dir / PICKLED_OUTPUTS_PATH)
            Path(temp_dir / "pytemp.py").write_text(contents)
            
            deps = " ".join([f"--with {dep}" for dep in self.requirements])
            pyversion = f"--python {self.python}" if self.python else ""
            quiet = "--quiet" if not self.debug else ""

            if self.debug:
                print(f"Running files in {temp_dir}")
                print(f"uv run --quiet {deps} {pyversion} {str(temp_dir / 'pytemp.py')}")
                with open(temp_dir / PICKLED_INPUTS_PATH, 'rb') as file:
                    args, kwargs = pickle.load(file)
                print(f"Pickled args: {args}")
                print(f"Pickled kwargs: {kwargs}")
                print(f"Contents of the script:\n\n {contents}")
            subprocess.run(f"uv run {quiet} {deps} {pyversion} {str(temp_dir / 'pytemp.py')}", shell=True, cwd=temp_dir)

            temp_pickle_path = os.path.join(temp_dir, "tmp.pickle")
            with open(temp_pickle_path, 'rb') as file:
                loaded_data = pickle.load(file)
        return loaded_data
