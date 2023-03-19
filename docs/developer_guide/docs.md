# Docs

The Docs were created using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/),
a Markdown static site generator with a material design theme.

## Running Docs Locally

1. Create and use the `dev` [development environment](./contributing.md#tox-development-environments)
2. Run the development server: `mkdocs serve`
    - If you are using VS Code, see the [VS Code Integration page](./vscode.md#docs)

## Building for Offline Usage

To build for offline usage, uncomment the `offline` plugin in `mkdocs.yml`
before running `mkdocs build`. For what this does, refer to
[the related Material for Mkdocs docs page](https://squidfunk.github.io/mkdocs-material/setup/building-for-offline-usage/).

## Features

### Automatic Documentation from Sources

[mkdocstrings](https://mkdocstrings.github.io/) was used to create the Code Reference
section of the Docs.

!!! warning "incompatible `theme.features`"

    mkdocstrings is not compatible with
    [`theme.features.navigation.indexes`](https://squidfunk.github.io/mkdocs-material/setup/setting-up-navigation/#section-index-pages).

### Versioning

The Docs site has the following versions:

- Version from branches
    - `main`: aliased to `latest`
        - Whenever you are on a version other than `latest`, a warning will be displayed
          above the header
    - `pr-<pr number>`:
        - Created when a pull request is opened
        - Updated when the pull request commits are modified
        - Deleted when the pull request is closed
- Version from releases: `<x.x>`
