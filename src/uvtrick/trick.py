import subprocess
import pickle
from pathlib import Path
import tempfile

__all__ = ("uvtrick_",)

template = """
if __name__ == "__main__":
    import pickle
    with open('tmp.pickle', 'wb') as f:
        pickle.dump({func}({string_args} {string_kwargs}), f)
"""


def uvtrick_(path, func, *args, **kwargs):
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

        code += template.format(
            func=func,
            string_args=string_args,
            string_kwargs=string_kwargs,
        )
        script.write_text(code)
        # print(code)

        cmd = ["uv", "run", "--quiet", str(script)]
        subprocess.run(cmd, cwd=temp_dir, check=True)

        return pickle.loads(output.read_bytes())
