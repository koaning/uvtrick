from uvtrick import load, Env

hello = load("tests/rich-script.py", "hello")

print(hello())

add = load("tests/rich-script.py", "add")

print(add(1, 2))
print(add(a=1, b=2))

def uses_rich(a, b):
    from rich import print
    print("hello")
    return a + b

# This runs the function `uses_rich` in a new environment with the `rich` package installed.
# Just like the `load` function, the result is returned via pickle. 
for version in (10, 11, 12, 13):
    Env(f"rich=={version}", python="3.12").run(uses_rich, a=1, b=2)
