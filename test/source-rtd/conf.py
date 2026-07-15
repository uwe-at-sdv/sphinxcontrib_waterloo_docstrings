# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Smoke'
copyright = '2026, Uwe'
author = 'Uwe'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
	"sphinxcontrib.waterloo_docstrings"
	]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Path setup ------------------------------------------------

# If your modules are located outside the documentation directory,
# add their paths here. Use os.path.abspath to convert relative
# paths to absolute ones if necessary.
import os,sys

ROOT = os.path.abspath("../../examples-python")
sys.path.insert(0, ROOT)
print("ROOT:", ROOT)
