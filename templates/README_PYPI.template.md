_README_LOGO_

# Sphinx-Contrib Waterloo Docstrings

_BADGES_

_README_COMMON_

## Installation

Install the Sphinx extension from PyPI:

```bash
pip install sphinxcontrib-waterloo-docstrings
```

The package depends on `sdv-doc-waterloo` and provides the Sphinx integration
layer for Waterloo Docstrings.

## Quick check

After installation, add the extension to a Sphinx `conf.py`:

```python
extensions = [
    "sphinxcontrib.waterloo_docstrings",
]
```
