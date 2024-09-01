import textwrap
import subprocess
import pickle
import inspect
from pathlib import Path
import tempfile
import os

from .core import maincall


PICKLED_INPUTS_PATH = "pickled_inputs.pickle"
PICKLED_OUTPUTS_PATH = "tmp.pickle"


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
            contents += maincall(
                func,
                temp_dir / PICKLED_INPUTS_PATH,
                temp_dir / PICKLED_OUTPUTS_PATH,
            )
            Path(temp_dir / "pytemp.py").write_text(contents)

            deps = " ".join([f"--with {dep}" for dep in self.requirements])
            pyversion = f"--python {self.python}" if self.python else ""
            quiet = "--quiet" if not self.debug else ""

            if self.debug:
                print(f"Running files in {temp_dir}")
                print(
                    f"uv run --quiet {deps} {pyversion} {str(temp_dir / 'pytemp.py')}",
                )
                with open(temp_dir / PICKLED_INPUTS_PATH, "rb") as file:
                    args, kwargs = pickle.load(file)
                print(f"Pickled args: {args}")
                print(f"Pickled kwargs: {kwargs}")
                print(f"Contents of the script:\n\n {contents}")
            subprocess.run(
                f"uv run {quiet} {deps} {pyversion} {str(temp_dir / 'pytemp.py')}",
                shell=True,
                cwd=temp_dir,
            )

            temp_pickle_path = os.path.join(temp_dir, "tmp.pickle")
            with open(temp_pickle_path, "rb") as file:
                loaded_data = pickle.load(file)
        return loaded_data
