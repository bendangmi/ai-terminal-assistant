.PHONY: all install dev-install clean test lint type check format docs build publish help

PYTHON := python
PIP := pip
PYTEST := pytest
BLACK := black
ISORT := isort
FLAKE8 := flake8
MYPY := mypy
TOX := tox
MKDOCS := mkdocs

help:
	@echo "Available commands:"
	@echo "  install      Install package"
	@echo "  dev-install Install package in development mode with all extras"
	@echo "  clean       Clean build artifacts"
	@echo "  test        Run tests"
	@echo "  lint        Run linting"
	@echo "  type        Run type checking"
	@echo "  check       Run all checks (lint, type, test)"
	@echo "  format      Format code"
	@echo "  docs        Build documentation"
	@echo "  build       Build package"
	@echo "  publish     Publish package to PyPI"

install:
	$(PIP) install .

dev-install:
	$(PIP) install -e ".[dev,docs]"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .tox/
	rm -rf site/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	find . -type f -name ".DS_Store" -delete

test:
	$(PYTEST) tests/ -v --cov=ata --cov-report=term-missing

lint:
	$(BLACK) --check .
	$(ISORT) --check-only .
	$(FLAKE8) .

type:
	$(MYPY) ata tests

check: lint type test

format:
	$(BLACK) .
	$(ISORT) .

docs:
	$(MKDOCS) build

serve-docs:
	$(MKDOCS) serve

build: clean
	$(PYTHON) -m build

publish: build
	$(PYTHON) -m twine upload dist/*

# Windows compatibility
ifeq ($(OS),Windows_NT)
    RM = rd /s /q
    RMDIR = rd /s /q
    MKDIR = mkdir
    PYTHON = python
else
    RM = rm -f
    RMDIR = rm -rf
    MKDIR = mkdir -p
    PYTHON = python3
endif 