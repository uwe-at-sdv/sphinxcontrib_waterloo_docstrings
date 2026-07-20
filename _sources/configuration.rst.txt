Configuration
=============

Path setup
----------

.. code:: python

	# If extensions (or modules to document with autodoc) are in another directory,
	# add these directories to sys.path here. If the directory is relative to the
	# documentation root, use os.path.abspath to make it absolute, like shown here.
	#
	import os
	import sys
	from pathlib import Path

	CONF_DIR = Path(__file__).resolve().parent
	ROOT_DIR = CONF_DIR.parents[1]

	# For our examples
	examples = str((ROOT_DIR / "examples-python").resolve())
	sys.path.insert(0, examples)

Diagnostics
-----------

* :wtrl_var:`wtrl_diagnostics_color`: bool, default False - Render WTRL diagnostics in document.
* :wtrl_var:`wtrl_diagnostics_embed`: bool, default False - Render WTRL diagnostics in color.
* :wtrl_var:`wtrl_verbose_current_object`: bool default False - druckt zu Beginn des Renderings den qualifizierten Identifier in die Sphinxausgabe.
* :wtrl_var:`wtrl_verbose_state_change`: bool default True - druckt Meldung bei wtrl_{push|pop}_current_{scope|module|class}


