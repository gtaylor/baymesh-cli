default: lint test

install:
	uv sync

lint:
	uv run ruff check

fmt:
	uv run ruff format

test:
	uv run pytest tests
