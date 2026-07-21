.. _chapter_misc:

Miscellaneous
=============

Escaping
--------

In this section we test how special reST characters are handled by the
Sphinx backend. The goal is to avoid letting the backend influence the
Waterloo syntax. Internally, this means that we have to escape critical
reST characters. Our test module is:

.. literalinclude:: ../../examples-python/doc_escape.py
	:language: python
	:tab-width: 4

The docstring is rendered as follows:

.. wtrl_autodoc_module:: doc_escape

Certain edge cases, such as the section "Malformed Waterloo", are expected to
be problematic in the browser rendering as well. In practice, that only
matters in the unusual meta-case where you want to explain "wrong" Waterloo
syntax in a docstring.

Itemization
-----------

.. literalinclude:: ../../examples-python/doc_enumeration.py
	:language: python
	:tab-width: 4

.. wtrl_autodoc_function:: doc_enumeration.myfunc

