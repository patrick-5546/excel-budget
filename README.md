# A sample Python project

<!-- [![PyPI][versionbadge]][packageurl] -->
[![Test][testbadge]][testfile]
![Coverage][covbadge]

<!-- ![PyPI - Python Version][pyversionbadge] -->
[![GitHub][licensebadge]][licenseurl]

<!-- [versionbadge]: https://img.shields.io/pypi/v/excelbudget -->
<!-- [packageurl]: https://pypi.org/project/excelbudget/ -->
[testbadge]: https://github.com/patrick-5546/excelbudget/actions/workflows/ci.yml/badge.svg
[testfile]: https://github.com/patrick-5546/excelbudget/actions/workflows/ci.yml
[covbadge]: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/patrick-5546/845b19d91f3d03c94677f6fae6eb414c/raw/covbadge-excelbudget.json
<!-- [pyversionbadge]: https://img.shields.io/pypi/pyversions/excelbudget -->
[licensebadge]: https://img.shields.io/github/license/patrick-5546/excelbudget
[licenseurl]: https://github.com/patrick-5546/excelbudget/blob/main/LICENSE

![Python Logo](https://www.python.org/static/community_logos/python-logo.png "Sample inline image")

A sample project that exists as an aid to the [Python Packaging User
Guide][packaging guide]'s [Tutorial on Packaging and Distributing
Projects][distribution tutorial].

This project does not aim to cover best practices for Python project
development as a whole. For example, it does not provide guidance or tool
recommendations for version control, documentation, or testing.

[The source for this project is available here][src].

The metadata for a Python project is defined in the `pyproject.toml` file,
an example of which is included in this project. You should edit this file
accordingly to adapt this sample project to your needs.

---

This is the README file for the project.

The file should use UTF-8 encoding and can be written using
[reStructuredText][rst] or [markdown][md] with the appropriate [key set][md
use]. It will be used to generate the project webpage on PyPI and will be
displayed as the project homepage on common code-hosting services, and should be
written for that purpose.

Typical contents for this file would include an overview of the project, basic
usage examples, etc. Generally, including the project changelog in here is not a
good idea, although a simple “What's New” section for the most recent version
may be appropriate.

[packaging guide]: https://packaging.python.org
[distribution tutorial]: https://packaging.python.org/tutorials/packaging-projects/
[src]: https://github.com/patrick-5546/excelbudget
[rst]: http://docutils.sourceforge.net/rst.html
[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"
[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional

## Using this Template Repository

This fork of [pypa/sampleproject](https://github.com/pypa/sampleproject) adds
pinned dependency management, a documentation site, VS Code integration,
improved GitHub integration, and much more.

After creating a repository using this template, some files need to be updated to
make it your own:

### Update Repository and Package Names

1. Find and replace `patrick-5546/sampleproject` with the owner and name of your repository
2. Rename the directory `src/sample/` to the name of your package
3. Find and replace `sample` with the name of your package

### Update README Badges

1. In `README.md`, update `testbadge`, `testfile`, `licensebadge`, and `licenseurl`
   with the repository owner and name where applicable
2. Create an empty gist named `covbadge.json` and copy its ID
3. In `README.md`, update `covbadge` with the repository owner and gist ID where applicable
4. In `.github/workflows/tests.yml`, update the "Make badge" step of "Coverage" with the
   repository owner, repository name, and gist ID where applicable
5. Create a GitHub personal access token with the "gist" scope and copy its value
6. Create a repository secret named `GIST_TOKEN` and paste the token

### Update Infrastructure

1. In `.github/CODEOWNERS`, update code owners accordingly

## Setup Docs

Some manual setup is required to publish the Docs using GitHub pages:

1. Setup the `main` version of the Docs
   1. Create and use the `dev` [development environment](https://patrick-5546.github.io/sampleproject/main/developer_guide/contributing/#tox-development-environments),
      running the commands below in it
   2. Switch to the main branch if you are not already in it: `git switch main`
   3. Create the `main` version and alias it to `latest`:
      `mike deploy --update-aliases main latest`
   4. Make `latest` the default version: `mike set-default latest`
   5. Push the `gh-pages` branch: `git switch gh-pages` then `git push`
2. In the repository settings for Pages, set the branch to `gh-pages`

For more details about versioning, search for "versioning" in the Docs.

### Update README

In `README.md`,

1. update the title and
2. delete everything after the badge URLs
