from pathlib import Path
from uvtrick import load

tests_dir = Path(__file__).parents[1] / "tests" / "assets"
script = tests_dir / "rich_script.py"

add = load(script, "add")

print(f"{add(1, 2)=}")
print(f"{add(a=1, b=2)=}")
