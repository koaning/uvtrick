from uvtrick import Env

rich_versions = (10, 11, 12, 13)
print(f"Now iterating through {rich_versions=}:")


def uses_rich(a, b):
    from rich import print
    from importlib import metadata

    version = metadata.version("rich")

    print(f"hello from rich=={version}")
    return a + b


# This runs the function `uses_rich` in a new environment with the `rich` package installed.
# Just like the `load` function, the result is returned via pickle.
for version in rich_versions:
    result = Env(f"rich=={version}", python="3.12").run(uses_rich, a=1, b=2)
    print(f" --> add(1, 2) = {result}")
