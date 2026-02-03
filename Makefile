.PHONY: test lint format

test:
	uv run coverage run manage.py test --testrunner=dvd_rental.test_runner.ExistingDBTestRunner
	uv run coverage report -m

lint:
	uv run ruff check .

format:
	uv run ruff check . --fix
