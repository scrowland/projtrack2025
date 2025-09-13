.PHONY: run lint

run:
	uv run fastapi dev projtrack/main.py

lint:
	uv run ruff format .
	uv run ruff check .
	uv run mypy projtrack/