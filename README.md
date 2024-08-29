<img src="docs/highlight.png" width="125" height="125" align="right" />

### uvtrick

> A super duper hacky demo of a trick, via `uv` and pickle, to run Python code in another venv ... from Python.

## Quickstart 

You can install this tool via: 

```
uv pip install uvtrick
```

## Usage: 

```python
from uvtrick import load

# Load the function `hello` from the file `some_script.py`
# It runs in another virtualenv, but you get back the response via pickle. 
# Be aware of the limitations, please only consider base Python objects.
add = load("some_script.py", "add")

# This result is from the `some_script.py` file, running in another virtualenv 
# with `uv`. A pickle in a temporary file is used to communicate the result.
add(1, 2)  # 3
```

Note that this approach is more of a demo, it is very hacky, should probably not be taken serious and it assumes that the Python script in question uses inline script metadata. More information on this feature can be found here:

- https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies
- https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata
