<p align="center">
	<img src="https://raw.githubusercontent.com/uwe-at-sdv/sphinxcontrib_waterloo_docstrings/main/img/wtrl_sphinx_logo_color.svg" alt="Waterloo Logo" width="220">
</p>

# Sphinx-Contrib Waterloo Docstrings

![License](https://img.shields.io/badge/license-BSD--2--Clause-EEEAE0)
![Version](https://img.shields.io/badge/version-0.7.10-D4AF37)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)
![Sphinx](https://img.shields.io/badge/Sphinx-extension-0A507A)
[![WTRL](https://img.shields.io/badge/%28%E2%9A%96%29-Waterloo--Docstrings-932725)](https://github.com/uwe-at-sdv/sdv_doc_waterloo)
[![PyPI](https://img.shields.io/badge/PyPI-sphinxcontrib--waterloo--docstrings-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/sphinxcontrib-waterloo-docstrings/)

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

## Install from source

Install from a local checkout:

```bash
pip install .
```

For development, use an editable install:

```bash
pip install -e .
```

Install directly from the GitHub repository:

```bash
pip install "git+https://github.com/uwe-at-sdv/sphinxcontrib_waterloo_docstrings.git"
```

## Build the theme showcase

The test documentation can be built for the supported showcase themes:

```bash
cd test
make html-furo
make html-alabaster
make html-classic
```
