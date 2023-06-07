# Miscellaneous Python Tools

A batch of Miscellaneous Python Tools

[![GitHub](https://img.shields.io/github/license/misc/misc)](https://github.com/misc/misc/blob/main/LICENSE)
[![CI Status](https://github.com/misc/misc/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/misc/misc/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/misc/misc/branch/main/graph/badge.svg?token=4JPKXI122N)](https://codecov.io/gh/misc/misc)
[![Documentation Status](https://readthedocs.org/projects/misc/badge/)](https://misc.readthedocs.io/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Serious Scaffold Python](https://img.shields.io/badge/serious%20scaffold-python-blue)](https://github.com/huxuan/serious-scaffold-python)
[![PyPI](https://img.shields.io/pypi/v/misc)](https://pypi.org/project/misc/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/misc)](https://pypi.org/project/misc/)

<div align="center">
  <a href="https://github.com/misc/misc">
    <img src="docs/_static/images/logo.png" height=300 alt="Miscellaneous Python Tools">
  </a>
</div>

Many efforts have been made to ease the project setup, but most of them are only language-specified basic components. In practice, we have to deal with much more details, especially for team projects. Many commonly used tools and configurations need to be handled properly. Moreover, different people tend to have different favors in various aspects. If you are tired of the inefficient setup process and endless discussion, [Serious Scaffold Python](https://github.com/huxuan/serious-scaffold-python) is here to terminate those for Python Projects.

If you find this helpful, please consider [sponsorship](https://github.com/sponsors/huxuan).

## Features

- Basic Python project structure as a package with tests and documentation.
- Categorized requirements management with constraints for different environments.
- [`typer`](https://github.com/tiangolo/typer) for CLI with tests and automatic documentation generation.
- [`pydantic`](https://github.com/pydantic/pydantic) for [settings](https://pydantic-docs.helpmanual.io/usage/settings/) with tests and documentation as module samples.
- [`setuptools-scm`](https://github.com/pypa/setuptools_scm/) to extract the version for the package.
- [`black`](https://github.com/psf/black), [`isort`](https://pycqa.github.io/isort/), [`mypy`](http://www.mypy-lang.org/), [`ruff`](https://github.com/charliermarsh/ruff) and [`toml-sort`](https://github.com/pappasam/toml-sort) as linters.
- [`pre-commit`](https://github.com/pre-commit/pre-commit) with [general hooks](https://github.com/pre-commit/pre-commit-hooks) and local linters.
- `Makefile` as the entry point for common actions.
- VSCode settings with recommended extensions.
- GitHub workflows for lint, tests, package and documentation preview.

## Quickstart

1. [Install Copier](https://copier.readthedocs.io/en/stable/#installation).
1. Install the necessary tools for development: `pipenv` and `pre-commit`.
1. Generate the project with the `copier` command.

   ```
   copier gh:huxuan/serious-scaffold-python /path/to/project
   ```

1. Initialize the project with the `git` and `make` commands.

   ```
   cd /path/to/project
   git init
   git add .
   make dev
   make pre-commit
   git commit -a -m "Init from serious-scaffold-python."
   ```

1. Happy hacking.

## Roadmap

- More detailed documentation for usage.
- More detailed documentation for features.
- Add logging module.
- Refine README template.
- [Github Automatically generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes) integration.
- [GitHub Dependabot](https://github.com/dependabot) integration.
- [GitHub issue and pull request templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests).
- [Gitlab CI/CD](https://docs.gitlab.com/ee/ci/) integration.
- [Gitlab issue and merge request templates](https://docs.gitlab.com/ee/user/project/description_templates.html).

## License

MIT

## Contributing

Any suggestions, discussions and bug fixing are all welcome.
