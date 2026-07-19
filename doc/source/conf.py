# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

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

wtrl_diagnostics_color = True
wtrl_diagnostics_embed = True
wtrl_verbose_current_object = True
wtrl_verbose_state_change = True

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
exclude_patterns = []



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

def build_prolog_method_overview(ctx) -> List[nodes.Node]:
	return [nodes.rubric(text="Public methods")]

def build_prolog_method_block(ctx,parent : nodes.Node,class_obj,meth_obj : Callable) -> List[nodes.Node]:
	return ctx.parse(parent,0,f":wtrl_method_signature:`{class_obj.__name__}.{meth_obj.__name__}`")

def setup(app: Any) -> dict[str, Any]:
	app.add_lexer('python', PythonWaterlooLexer)
	app.add_lexer('python-waterloo', PythonWaterlooLexer)
