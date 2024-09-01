from pathlib import Path
from uvtrick import load

tests_dir = Path(__file__).parents[1] / "tests"
script = tests_dir / "rich_script.py"

hello = load(script, "hello")

print(f"{hello()=}")
