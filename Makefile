.PHONY: docs

install:
	uv pip install -e ".[dev]"

pypi:
	uv build
	uv publish --token 