.. _chapter_getting_started:

Getting Started
===============

This chapter shows the minimal path from a Python module with a Waterloo
docstring to rendered Sphinx documentation. It assumes a small project and uses
explicit placeholder paths so that the individual steps remain easy to adapt.

The goal is not to explain every Sphinx option. The goal is to create a working
documentation build that loads :wtrl_pkg:`sphinxcontrib-waterloo-docstrings`,
finds your Python module, and renders one Waterloo docstring.


Choose The Directories
----------------------

The examples below use two placeholder directories:

* :wtrl_file:`/path/to/PROJECT_DIR` -- the directory that contains the Python
  module you want to document.
* :wtrl_file:`/path/to/DOC_DIR` -- the directory in which the Sphinx
  documentation project will be created.

The module used in this tutorial is called :wtrl_mod:`my_module`. Its source
file is therefore:

.. code-block:: text

	/path/to/PROJECT_DIR/my_module.py

Run the setup commands from :wtrl_file:`/path/to/DOC_DIR` unless noted
otherwise.


Create A Virtual Environment
----------------------------

Using a Python virtual environment is recommended for the first setup. It keeps
Sphinx, Waterloo, and related packages separate from the system-wide Python
installation.

Create the environment in :wtrl_file:`/path/to/DOC_DIR`:

.. code-block:: bash

	python3 -m venv venv_wtrl

Activate it with the command appropriate for your operating system and shell.

.. list-table:: Activation Commands
	:widths: 20 30 50
	:header-rows: 1

	* - Platform
	  - Shell
	  - Command
	* - **Unix** / **macOS**
	  - Bash / Zsh
	  - :wtrl_cmd:`source` :wtrl_file:`venv_wtrl/bin/activate`
	* -
	  - Fish
	  - :wtrl_cmd:`source` :wtrl_file:`venv_wtrl/bin/activate.fish`
	* -
	  - csh/tcsh
	  - :wtrl_cmd:`source` :wtrl_file:`venv_wtrl/bin/activate.csh`
	* - **Windows**
	  - PowerShell
	  - :wtrl_file:`./venv_wtrl/Scripts/Activate.ps1`
	* -
	  - Command Prompt
	  - :wtrl_file:`./venv_wtrl/Scripts/activate.bat`
	* -
	  - Git Bash
	  - :wtrl_cmd:`source` :wtrl_file:`venv_wtrl/Scripts/activate`

.. note::

	**Windows / PowerShell:** If activation fails because of the execution
	policy, allow script execution for the current user:

	:wtrl_cmd:`Set-ExecutionPolicy` :wtrl_opt:`-ExecutionPolicy` :wtrl_value:`RemoteSigned` :wtrl_opt:`-Scope` :wtrl_value:`CurrentUser`

Leave the environment with :wtrl_cmd:`deactivate` when you are finished.


Install The Extension
---------------------

Inside the activated virtual environment, make sure :wtrl_pkg:`pip` is
available and reasonably up to date:

.. code-block:: bash

	python3 -m pip install --upgrade pip

If :wtrl_cmd:`python3 -m pip` is not available inside the environment,
bootstrap it first:

.. code-block:: bash

	python3 -m ensurepip --upgrade

Install Sphinx and the Waterloo Sphinx extension:

.. code-block:: bash

	python3 -m pip install sphinx sphinxcontrib-waterloo-docstrings

The extension depends on :wtrl_pkg:`sdv-doc-waterloo`; this dependency is
installed automatically.


Create A Sphinx Project
-----------------------

Still in :wtrl_file:`/path/to/DOC_DIR`, create a directory for the Sphinx
project and switch into it:

.. code-block:: bash

	mkdir doc
	cd doc

Initialize the Sphinx project:

.. code-block:: bash

	sphinx-quickstart

For this tutorial, choose separate source and build directories:

.. code-block:: text

	> Separate source and build directories (y/n) [n]: y
	> Project name: My-Project
	> Author name(s): My-Name
	> Project release []: 0.0.1
	> Project language [en]:

Separate source and build directories are not required by Waterloo, but they
make the tutorial layout explicit and keep generated files out of the source
tree.

Build the generated Sphinx skeleton once:

.. code-block:: bash

	make clean && make html

Open the generated documentation in your browser:

:wtrl_url:`file:///path/to/DOC_DIR/doc/build/html/index.html`


Enable Waterloo In Sphinx
-------------------------

Add the extension to :wtrl_file:`/path/to/DOC_DIR/doc/source/conf.py`:

.. code-block:: python

	extensions = [
		# other extensions
		"sphinxcontrib.waterloo_docstrings",
		]

Tell the extension where your project sources are located:

.. code-block:: python

	wtrl_basedirs = [
		"/path/to/PROJECT_DIR",
		]

The paths listed in :wtrl_var:`wtrl_basedirs` are added to :wtrl_mod:`sys.path`
during the Sphinx build. Installed packages usually do not need an entry here;
local source directories usually do.


Add A Waterloo Docstring
------------------------

Create or edit :wtrl_file:`/path/to/PROJECT_DIR/my_module.py` and insert the
following module docstring:

.. code-block:: python

	r"""
	Preamble:
		profile:
			module
		normative_sections:
			Contract
	Contract:
		general:
			|Must| serve as an example for a Waterloo docstring.
	"""

Waterloo indentation may use either one tab or four spaces per indentation
level. The example above uses tabs because they make the logical structure
compact in source form.

Before rendering, validate the docstring:

.. code-block:: bash

	waterlint validate --basedir /path/to/PROJECT_DIR --obj my_module

The :wtrl_opt:`--obj` option expects a Python module, class, function, or method
identifier, not a filename.


Render The Docstring
--------------------

Add the Waterloo directive to a Sphinx source file, for example
:wtrl_file:`/path/to/DOC_DIR/doc/source/index.rst`:

.. code-block:: rst

	.. wtrl_autodoc_module:: my_module

Build the documentation again:

.. code-block:: bash

	make clean && make html

The generated HTML page should now contain a compact, structured rendering of
the module docstring.


Optional Theme Notes
--------------------

The extension ships default styles that work with the tested themes
:wtrl_mod:`classic`, :wtrl_mod:`alabaster`, and :wtrl_mod:`furo`. Theme-specific
styling is not required for the first build.

For :wtrl_mod:`alabaster`, the package contains an optional stylesheet that
varies the Alabaster theme. It adapts the page layout to documentation with
long section names, such as fully qualified identifiers, and has a visible
effect on the rendering of Waterloo docstring boxes:

.. code-block:: python

	html_css_files = [
		# other project stylesheets
		"waterloo_alabaster.css",
		]

Most themes support :wtrl_attr:`html_favicon`. If you do not provide your own
favicon, you may use the Waterloo favicon:

.. code-block:: python

	html_favicon = "_static/favicon.ico"

See :ref:`CSS Customization <customization>` for details about roles, dark-mode
variables, and generated CSS classes.
