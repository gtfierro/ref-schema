.PHONY: test

compile: model/*.ttl
	poetry run python tools/compile.py

test: compile
	poetry run pytest -s -vvvv

doc.html:
	poetry run pylode build/ref-schema.ttl -o doc.html -c true
