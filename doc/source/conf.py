# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from typing import Any

# -- Path setup --------------------------------------------------------------

# For wtrl_basedirs
from pathlib import Path

# -- Syntax Highlighting -----------------------------------------------------
from python_waterloo_lexer import PythonWaterlooLexer

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Sphinx: Waterloo Docstrings'
copyright = '2026, Uwe'
author = 'Uwe'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
	"sphinxcontrib.waterloo_docstrings",
	]

# litinc-start-config-variables
wtrl_diagnostics_admonitions_enabled = True
wtrl_diagnostics_logging_enabled = True
wtrl_diagnostics_color_enabled = True
wtrl_current_object_logging_enabled = False
wtrl_scope_filtered_object_placeholders_enabled = True
wtrl_state_change_admonitions_enabled = True
wtrl_state_change_logging_enabled = True
# litinc-end-config-variables

# Configure base directories of documented modules.
# Installed modules are found automatically because they
# are already in sys.path. For our examples we add the
# base dir explicitly. This conf.py is located in
# ${REPO}/doc/source, and the examples are located in
# ${REPO}/examples-python, so that's two up, one down.
CONF_DIR = Path(__file__).resolve().parent
path_to_examples = str((CONF_DIR / ".." / ".." / "examples-python").resolve())
wtrl_basedirs = [
	path_to_examples
	]


templates_path = ['_templates']
exclude_patterns: list[str] = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

html_theme_options = {
# Filename rel _static/
    'logo': 'wtrl_logo_color_64x64.png',
# Display project name below logo
    'logo_name': 'false',
# Optional: center align the logo/text
    'logo_text_align': 'left',
}

# Use the multi-size favicon resource for browser tabs and HiDPI displays.
html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
#	'waterloo_alabaster.css',
	'wtrl_doc_custom.css',
	]

pygments_style = 'autumn'
pygments_dark_style = "gruvbox-dark"

def setup(app: Any) -> dict[str, Any]:
	app.add_lexer('python', PythonWaterlooLexer)
	app.add_lexer('python-waterloo', PythonWaterlooLexer)
	return {}
