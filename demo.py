from uvtrick import load

hello = load("tests/rich-script.py", "hello")

print(hello())

add = load("tests/rich-script.py", "add")

print(add(1, 2))
print(add(a=1, b=2))
