# Contributing

This repository's infrastructure features pinned dependency management,
a documentation site, an automated release process, GitHub integration, VS Code integration,
and much more.

## Setup for Local Development

1. [Install tox](https://tox.wiki/en/latest/installation.html)
2. Clone the repository

## Tox

[tox](https://tox.wiki/en/latest/index.html) is used to automate and standardize testing
across local development environments and CI/CD pipelines.

### Tox Configuration

The tox configuration for this repository can be found in `tox.ini`.

### Tox Environments

Each tox environment accomplishes a specific purpose.
List all tox environments and their descriptions with `tox list`.

Details about each environment are given below:

- `py*`: for a particular python version, it
    1. checks if the package can be built (may be commented out),
    2. runs the linters,
    3. runs the test suite, and
    4. generates a coverage report source file `.coverage`
- `check-release`: checks that the package is ready to be released
- `coverage`: converts `.coverage` to human readable formats
    - `html`: used to create the Coverage Report page
    - `json`: used to create the coverage badge in the README
- `dev`: used to create a development environment with all dependencies installed
    - When in the development environment, the commands that are run in each environment
      can be run in your terminal
- `docs-build`: builds the docs to ensure that they are in a valid state
- `docs-serve`: runs the docs development server
- `format`: runs the formatters
- `update`: updates the [dependencies](#dependencies) without upgrading
- `upgrade`: updates the [dependencies](#dependencies)

#### Running Tox Environments

- `tox -e <environment>` will run a single environment
- `tox` will run all the default environments as noted by `tox list`
    - To set an environment as default, add it to `envlist` in `tox.ini`

Known issues running tox environments:

| Environment | Issue                                           | Solution                                                                                                                                                              |
| ----------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `coverage`  | `coverage combine` outputs "No data to combine" | `coverage` cannot be run independently, as it needs `.coverage` from `testenv`: run `tox` instead. If you are still getting this error, remove `.coverage` and rerun. |

#### Tox Development Environments

The `tox devenv` command will create a virtual environment and install the environment's
dependencies in it.

- To create a virtual environment with all dependencies installed,
  run `tox devenv -e dev .venv`.
- Using a virtual environment: [activate Python virtual environments](https://realpython.com/python-virtual-environments-a-primer/#activate-it)

## Dependencies

Dependencies are defined in `pyproject.toml`.
They are pinned and managed using [pip-tools](https://pip-tools.readthedocs.io/en/latest/).
The pinned dependencies can be found in `requirements/`.

### How to Add or Update Dependencies

1. To add a dependency, add it in `pyproject.toml`;
   where you add the dependency depends on what type of dependency it is:
    - Add project dependencies to the `dependencies` list
    - Add [environment](#tox-environments)-specific dependencies to the corresponding list
      below `[project.optional-dependencies]`
2. Run the `update` tox environment: `tox -e update`
    - If you want to upgrade dependencies as well, run this instead: `tox -e upgrade`
3. Verify that the tests still pass: `tox`
4. If you are using the development environment, recreate it: `tox devenv -e dev .venv`
5. Commit and push the changes
