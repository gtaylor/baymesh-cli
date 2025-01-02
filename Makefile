default: lint test

install:
	uv sync --all-extras --dev

lint: fmt
	uv run ruff check
	uv run pyright

fmt:
	uv run ruff format

test:
	uv run pytest tests
