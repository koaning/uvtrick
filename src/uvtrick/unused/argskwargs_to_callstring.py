__all__ = ("argskwargs_to_callstring",)


def argskwargs_to_callstring(func, *args, **kwargs):
    string_kwargs = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
    string_args = ", ".join([f"{a}" for a in args]) + ", " if args else ""
    return f"{func.__name__}({string_args} {string_kwargs})"
