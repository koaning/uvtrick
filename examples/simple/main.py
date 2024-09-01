from pathlib import Path
from uvtrick import load

# Load the function `add` from the file `some_script.py`
# It runs in another virtualenv, but you get back the response via pickle.
# Be aware of the limitations, please only consider base Python objects.
script = Path(__file__).parent / "some_script.py"
add = load(script, "add")

# This result is from the `some_script.py` file, running in another virtualenv
# with `uv`. A pickle in a temporary file is used to communicate the result.
result = add(1, 2)  # 3

assert result == 3
print(result)
