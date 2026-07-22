## Project Status

The project is under development, but seems to do what it is supposed to do.
feel free to dowload and try out.

## About

The `sphinxcontrib-waterloo-docstrings` package provides the Sphinx rendering
layer for Waterloo Docstrings.

Waterloo Docstrings define a structured docstring format with explicit section
semantics, normativity rules, and machine-readable output layers. This package
connects that format to Sphinx by providing roles, directives, and rendering
helpers for documentation projects that want to present Waterloo docstrings as
human-readable HTML.

The extension is intentionally theme-friendly. It lets Sphinx themes such as
Furo, Alabaster, and Classic provide most of the final layout, while the
extension supplies semantic CSS classes for Waterloo roles and generated
documentation structures.

## What it provides

- Sphinx roles for Waterloo inline markup.
- Directives for rendering modules, classes, functions, methods, and context scopes.
- Static CSS for Waterloo semantic roles.
- Theme showcase sources for Furo, Alabaster, and Classic.

## Related packages

- `sdv-doc-waterloo`: core parser, validator, renderer, `waterlint`, and MCP server.
- `python-waterloo-lexer`: Pygments lexer for Python files with Waterloo docstrings.

## Documentation showcase

The Sphinx extension documentation is published at:

- <https://uwe-at-sdv.github.io/sphinxcontrib_waterloo_docstrings/>

The Sphinx extension showcase is published under:

- <https://uwe-at-sdv.github.io/sphinxcontrib_waterloo_docstrings/showcase/furo/>
- <https://uwe-at-sdv.github.io/sphinxcontrib_waterloo_docstrings/showcase/alabaster/>
- <https://uwe-at-sdv.github.io/sphinxcontrib_waterloo_docstrings/showcase/classic/>
