from textwrap import dedent
import subprocess
import pickle
from inspect import getsource
from pathlib import Path
import tempfile
import os

from .core import maincall


PICKLED_INPUTS_FNAME = "pickled_inputs.pickle"
SCRIPT_FNAME = "pytemp.py"
PICKLED_OUTPUTS_FNAME = "tmp.pickle"


class Env:
    """Represents a virtual environment with a specific Python version and set of dependencies."""

    def __init__(self, *requirements, python=None, debug=False):
        self.requirements = requirements
        self.python = python
        self.debug = debug

    def run(self, func, *args, **kwargs):
        """Run a function in the virtual environment using uv."""

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            inputs = temp_dir / PICKLED_INPUTS_FNAME
            script = temp_dir / SCRIPT_FNAME
            output = temp_dir / PICKLED_OUTPUTS_FNAME

            # Let's first pickle the inputs
            inputs.write_bytes(pickle.dumps((args, kwargs)))

            # Now write the contents of the script
            contents = dedent(getsource(func)) + "\n\n" + maincall(func, inputs, output)
            script.write_text(contents)

            deps = [f"--with {dep}" for dep in self.requirements]
            pyversion = f"--python {self.python}" if self.python else ""
            quiet = "" if self.debug else "--quiet"

            cmd = ["uv", "run", quiet, *deps, pyversion, str(script)]
            if self.debug:
                print(f"Running files in {temp_dir}\n{cmd}")
                args, kwargs = pickle.loads(inputs.read_bytes())
                print(f"Pickled args: {args}")
                print(f"Pickled kwargs: {kwargs}")
                print(f"Contents of the script:\n\n{contents}")
            subprocess.run(cmd, shell=True, cwd=temp_dir)

            return pickle.loads(output.read_bytes())
