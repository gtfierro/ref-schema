.PHONY: test clean

build/ref-schema.ttl: model/*.ttl tools/compile.py
	mkdir -p build
	uv run python tools/compile.py

test: build/ref-schema.ttl
	uv run pytest -s -vvvv

clean:
	rm -rf build/

doc.html: build/ref-schema.ttl
	uv run pylode build/ref-schema.ttl -o doc.html -c true
