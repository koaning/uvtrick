from pathlib import Path
from uvtrick import load

test_assets = Path(__file__).parents[1] / "tests" / "assets"
script = test_assets / "rich_script.py"

hello = load(script, "hello")

print(f"{hello()=}")
