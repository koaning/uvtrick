from pathlib import Path
import sys

# Put root dir on the path so `pytest.importorskip` can run them
root_dir = Path(__file__).parents[1]
sys.path.append(str(root_dir))
