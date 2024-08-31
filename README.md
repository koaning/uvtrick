<img src="img.png" width="125" height="125" align="right" />

### uvtrick

> A super duper hacky demo of a trick, via `uv` and pickle, to run Python code in another venv ... into this one.

## Quickstart 

You can install this tool via: 

```
uv pip install uvtrick
```

## Usage: 

There are a few ways to use this library. The first one is to use the `load` function to point 
to a Python script that contains the function you want to use. This function assumes that the 
script carries [inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/). 

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

But you can also take it a step further and use the `Env` class to run a function in a specific environment. 

```python
from uvtrick import Env

# For illustration purposes, let's assume that rich is not part of the current environment. 
# Also note that all the imports happen inside of this function. 
def uses_rich():
    from rich import print
    print("hello")

# This runs the function `uses_rich` in a new environment with the `rich` package installed.
# Just like the `load` function, the result is returned via pickle. 
Env("rich", python="3.12").run(uses_rich, a=1, b=2)
```

This approach is pretty useful if you are interested in running the same function in different versions of 
a dependency to spot a performance regression. You might be able to do that via something like:

```python
from uvtrick import Env

def uses_rich(a, b):
    from rich import print
    print("hello")
    return a + b

# This runs the function `uses_rich` in a new environment with the `rich` package installed.
# Just like the `load` function, the result is returned via pickle. 
for version in (10, 11, 12, 13):
    Env(f"rich=={version}", python="3.12").run(uses_rich, a=1, b=2)
```

#### Warning

This is highly experimental work and merely the result of some recreational programming. At the moment everything is turned into
Python files in temporary directories so that `uv` can easily pick it up. We use pickle to communicate results back, but the function
inputs currently only work for integers and floats ... because these can be copied directly in plain text files. 

We are thinking about ways to do this more generally with pickles. All in due (recreational) time!
