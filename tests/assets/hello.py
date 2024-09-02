from pathlib import Path
from uvtrick import load

test_assets_dir = Path(__file__).parent
script = test_assets_dir / "rich_script.py"

hello = load(script, "hello")

print(f"{hello()=}")
