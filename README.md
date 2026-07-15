<p align="center">
	<img src="https://raw.githubusercontent.com/uwe-at-sdv/sdv_doc_waterloo/main/img/wtrl_logo_color.svg" alt="Waterloo Logo" width="220">
</p>

# Sphinx-Contrib Waterloo Docstrings

![License](https://img.shields.io/badge/license-BSD--2--Clause-blue)
![Version](https://img.shields.io/badge/version-0.3.2-orange)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Sphinx](https://img.shields.io/badge/Sphinx-extension-0A507A)
[![PyPI](https://img.shields.io/badge/PyPI-sphinxcontrib--waterloo--docstrings-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/sphinxcontrib-waterloo-docstrings/)

# This branch is under development

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

The public project documentation is published at:

- <https://uwe-at-sdv.github.io/sdv_doc_waterloo/>

The Sphinx extension showcase is planned under:

- <https://uwe-at-sdv.github.io/sdv_doc_waterloo/sphinx/furo/>
- <https://uwe-at-sdv.github.io/sdv_doc_waterloo/sphinx/alabaster/>
- <https://uwe-at-sdv.github.io/sdv_doc_waterloo/sphinx/classic/>

## Install from source

Install from a local checkout:

```bash
pip install .
```

For development, use an editable install:

```bash
pip install -e .
```

Install directly from the `sphinx` branch:

```bash
pip install "git+https://github.com/uwe-at-sdv/sdv_doc_waterloo.git@sphinx"
```

## Build the theme showcase

The test documentation can be built for the supported showcase themes:

```bash
cd test
make html-furo
make html-alabaster
make html-classic
```
