import subprocess
import pickle
from pathlib import Path
import tempfile
import os


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

        code += f"""if __name__ == "__main__":
    import pickle
    with open('tmp.pickle', 'wb') as f:
        pickle.dump({func}({string_args} {string_kwargs}), f)\n"""

        Path(temp_dir / "pytemp.py").write_text(code)

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
