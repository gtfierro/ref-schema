.PHONY: test

compile: model/*.ttl
	uv run python tools/compile.py

test: compile
	uv run pytest -s -vvvv

doc.html:
	uv run pylode build/ref-schema.ttl -o doc.html -c true
