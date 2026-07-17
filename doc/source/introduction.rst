Introduction
============

Diese Extension stellt Direktiven und Roles bereit,
mit denen man Docstrings im Waterloo-Format in HTML rendern kann.

Project status
--------------

We use :wtrl_cmd:`mypy` for static typechecking. The source file(s)

.. literalinclude:: type_checking_files.txt
	:language: none

are validated on a regular basis. The current status is

.. literalinclude:: type_checking_report.txt
	:language: none

Our :wtrl_lit:`mypy`-configuration is:

.. literalinclude:: ../../mypy.ini
	:language: ini

Exceptions from typechecking are:

.. literalinclude:: type_checking_exceptions.txt
	:language: none



Installation
============

.. code:: bash

	pip install sphinxcontrib-waterloo-docstrings


Quick Start
===========

Do this

.. code:: bash

	sphinx-quickstart

and fill in what you need for yout test.

In conf.py

.. code:: python

	extensions = [
		# begin your other extensions
		...
		# end your other extensions
		"sphinxcontrib.waterloo_docstrings",
		]

Run this command which generates a simple demo chapter:

.. code:: bash

	wtrl_quickstart

Then

.. code:: bash

	make html

or in order to clean caches if there are any:

.. code:: bash

	make clean && make html


HTML-Theme-Options
==================

For theme :wtrl_mod:`Alabaster`
-------------------------------

Additional CSS
~~~~~~~~~~~~~~

Our modest modifications to the Alabaster theme, which make no claim
to typographical accuracy, but provide more space for the table of contents.

.. code:: python

	html_css_files = [
		# begin your other style sheets
		...
		# end your other style sheets
		'waterloo_alabaster.css',
		]


For theme :wtrl_mod:`Furo`
--------------------------

Favicon
=======

If you don't feel like designing you own one, maybe add
the default Waterloo favicon:

.. code:: python

	html_favicon = '_static/favicon.ico'

