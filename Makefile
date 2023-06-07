.PHONY: clean deepclean install dev version pre-commit lint black mypy ruff toml-sort tests freeze build upload docs docs-autobuild

# Construct pipenv run command with or without site-packages flag when not in CI environment and pipenv command exists.
SITE_PACKAGES_FLAG = $(shell [ "${SS_SITE_PACKAGES}" = "true" ] && echo --site-packages)
PIPRUN := $(shell [ "${CI}" != "true" ] && command -v pipenv > /dev/null 2>&1 && echo pipenv ${SITE_PACKAGES_FLAG} run)

# Remove common intermediate files.
clean:
	-rm -rf \
		.coverage \
		.mypy_cache \
		.pytest_cache \
		.ruff_cache \
		Pipfile* \
		coverage.xml \
		dist \
		docs/_build
	find . -name '*.egg-info' -print0 | xargs -0 rm -rf
	find . -name '*.pyc' -print0 | xargs -0 rm -f
	find . -name '*.swp' -print0 | xargs -0 rm -f
	find . -name '.DS_Store' -print0 | xargs -0 rm -f
	find . -name '__pycache__' -print0 | xargs -0 rm -rf

deepclean: clean
	-pre-commit uninstall --hook-type pre-push
	-pipenv --venv >/dev/null 2>&1 && pipenv --rm

install:
	${PIPRUN} pip install -e . -c constraints/$(or $(SS_CONSTRAINTS_VERSION),default).txt

dev-%:
	${PIPRUN} pip install -e .[$*] -c constraints/$(or $(SS_CONSTRAINTS_VERSION),default).txt

dev:
	${PIPRUN} pip install -e .[docs,lint,package,tests] -c constraints/$(or $(SS_CONSTRAINTS_VERSION),default).txt
	-[ "${CI}" != "true" ] && pre-commit install --hook-type pre-push

version:
	${PIPRUN} python -m setuptools_scm

pre-commit:
	pre-commit run --all-files

black:
	${PIPRUN} python -m black docs tests src

lint: isort mypy ruff toml-sort

isort:
	${PIPRUN} python -m isort .

mypy:
	${PIPRUN} python -m mypy docs tests src

ruff:
	${PIPRUN} python -m ruff docs tests src

toml-sort:
	${PIPRUN} toml-sort pyproject.toml

tests:
	${PIPRUN} python -m pytest .

freeze:
	@${PIPRUN} pip freeze --exclude-editable

build:
	${PIPRUN} python -m build

upload:
	${PIPRUN} python -m twine upload dist/*

docs:
	${PIPRUN} python -m sphinx.cmd.build docs docs/_build

docs-autobuild:
	${PIPRUN} python -m sphinx_autobuild docs docs/_build
