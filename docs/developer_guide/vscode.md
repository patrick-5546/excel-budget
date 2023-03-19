# VS Code

## Setup for VS Code

1. `cd` to the root directory of the repository
2. Create the `dev` [development environment](./contributing.md#tox-development-environments):
   `tox devenv -e dev .venv`
3. Open the repository in VS Code: `code .`
4. Install the recommended extensions

## Configuration Files

VS Code configuration files can be found in the `.vscode/` directory.

- `cspell.json`: configuration for the spell checker
- `extensions.json`: recommended extensions
    - See the recommended extensions by searching for "@recommended" in the Extensions view
- `google_docstring_custom_template.mustache`: a custom docstrings template for
  [autoDocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
  until [this issue](https://github.com/NilsJPWerner/autoDocstring/issues/232) is resolved
- `launch.json`: launch configurations
    - Run the launch configurations from the Run and Debug view
- `settings.json`: settings

## Shortcuts

Useful VS Code shortcuts that aren't specific to this repository.

!!! tip "MacOS Shortcuts"

    For keyboard shortcuts on MacOS, substitute ++ctrl++ with ++cmd++.

- Open Quick Open: ++ctrl+p++
    - Search for files
    - Open the command palette by typing "> "
    - Search for tasks by typing "task "
    - Search for launch configurations by typing "debug "
- Open Command Palette: ++ctrl+shift+p++

## Integrations

### Docs

Related recommended extensions enhance Markdown file previews, check for markdownlint errors,
enhance VS Code Markdown support, add autocomplete for `mkdocs.yml`, and more:

- The enhanced Markdown file preview replaces VS Code's built-in preview
- The configuration file for markdownlint is `.markdownlint.json`
- Format tables in a Markdown file with ++alt+shift+f++
    - On Linux, the shortcut is ++ctrl+shift+i++

There are also launch configurations to run the development server and open browsers:

| Launch Configuration | Description                                         |
| -------------------- | --------------------------------------------------- |
| Serve Docs           | runs `mkdocs serve`                                 |
| Open Docs in Chrome  | runs `mkdocs serve` and open Docs in Chrome         |
| Open Docs in Edge    | runs `mkdocs serve` and open Docs in Microsoft Edge |

### Python

Related recommended extensions improve autocomplete, format on save, lint, test, and more:

- Adds autocomplete for docstrings, type hints, and functions
- Runs the [black](https://pypi.org/project/black/) and [isort](https://pypi.org/project/isort/)
  formatters when a file is saved
- Runs the [flake8](https://pypi.org/project/flake8/) and [mypy](https://pypi.org/project/mypy/)
  linters when a file is saved and after formatters run
- Run tests from the Testing view

### Common Extensions & Settings

Other recommended extensions further improve autocomplete (AI, file paths), check spelling,
and show the commit and author who last modified the current line, and more:

- Mark a word as spelled correct by hovering over it, selecting `Quick Fix...`,
  then selecting `Add "<word>" to config: .vscode/cspell.json`
- Hover over the current line blame annoation at the end of the line for more details

Common settings:

- Make whitespace at the end of the line visible
- Ruler at the line length limit
