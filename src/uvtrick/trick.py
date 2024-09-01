import subprocess
import pickle
from pathlib import Path
import tempfile
import os

__all__ = ("uvtrick_",)


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
        subprocess.run(
            f"uv run --quiet {str(temp_dir / 'pytemp.py')}",
            shell=True,
            cwd=temp_dir,
        )

        temp_pickle_path = os.path.join(temp_dir, "tmp.pickle")
        with open(temp_pickle_path, "rb") as file:
            loaded_data = pickle.load(file)
    return loaded_data