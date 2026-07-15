_README_LOGO_

# Sphinx-Contrib Waterloo Docstrings

_BADGES_

_README_COMMON_

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
