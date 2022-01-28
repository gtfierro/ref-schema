.PHONY: test

compile: model/*.ttl test
	poetry run python tools/compile.py

test:
	poetry run pytest -s -vvvv
