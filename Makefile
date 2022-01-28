.PHONY: test

compile: *.ttl test
	poetry run python compile.py

test: compile
	poetry run pytest -s -vvvv
