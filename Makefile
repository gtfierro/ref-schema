.PHONY: test

compile: model/*.ttl test
	poetry run python tools/compile.py

test:
	poetry run pytest -s -vvvv

docs: compile
	poetry run pylode build/ref-schema.ttl -o doc.html -c true
