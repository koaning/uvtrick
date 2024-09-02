from pathlib import Path
from uvtrick import load

test_assets_dir = Path(__file__).parent
script = test_assets_dir / "rich_script.py"

add = load(script, "add")

print(f"{add(1, 2)=}")
print(f"{add(a=1, b=2)=}")
