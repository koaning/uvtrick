from textwrap import dedent
import subprocess
import pickle
from inspect import getsource
from pathlib import Path
import tempfile

from .core import maincall

__all__ = ("Env",)


class Env:
    """Represents a virtual environment with a specific Python version and set of dependencies."""

    def __init__(self, *requirements: str, python: str = None, debug: bool = False):
        self.requirements = requirements
        self.python = python
        self.debug = debug
        self.temp_dir: Path = None

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
        quiet = "" if self.debug else "--quiet"
        deps = [f"--with {dep}" for dep in self.requirements]
        pyversion = f"--python {self.python}" if self.python else ""
        return ["uv", "run", quiet, *deps, pyversion, str(self.script)]

    def report(self, contents: str) -> None:
        print(f"Running files in {self.temp_dir}\n{self.cmd}")
        args, kwargs = pickle.loads(self.inputs.read_bytes())
        print(f"Pickled args: {args}")
        print(f"Pickled kwargs: {kwargs}")
        print(f"Contents of the script:\n\n{contents}")
        return

    def run(self, func, *args, **kwargs):
        """Run a function in the virtual environment using uv."""

        with tempfile.TemporaryDirectory() as temp_dir:
            self.temp_dir = Path(temp_dir)
            inputs, script, output = self.inputs, self.script, self.output

            # Let's first pickle the inputs
            self.inputs.write_bytes(pickle.dumps((args, kwargs)))

            # Now write the contents of the script
            contents = dedent(getsource(func)) + "\n\n" + maincall(func, inputs, output)
            script.write_text(contents)

            # Finally run the `uv run` command in a shell subprocess
            if self.debug:
                self.report(contents)
            subprocess.run(self.cmd, shell=True, cwd=temp_dir)

            return pickle.loads(output.read_bytes())
