from functools import wraps
from uvtrick import Env

def with_package_versions(package_name, versions, python_version="3.12"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for version in versions:
                env = Env(f"{package_name}=={version}", python=python_version)
                result = env.run(func, *args, **kwargs)
                results.append((version, result))
            return results

        return wrapper

    return decorator


@with_package_versions("rich", versions=[10, 11, 12, 13])
def test_rich(a, b):
    from rich import print
    from importlib import metadata

    version = metadata.version("rich")
    print(f"Hello from rich=={version}")
    return a + b

if __name__ == "__main__":
    results = test_rich(1, 2)
    for version, result in results:
        print(f"Rich version {version}: add(1, 2) = {result}")
