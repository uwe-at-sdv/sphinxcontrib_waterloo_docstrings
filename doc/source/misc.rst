.. _chapter_misc:

Miscellaneaous
==============

Escaping
--------

In diesem Abschnitt testen wir, wie spezielle reST-Zeichen
im Sphinx-Backend behandelt werden. Das Ziel ist, zu vermeiden,
dass die Waterloo-Syntax durch das Backend beeinflusst wird.
Intern bedeutet das, dass wir kritische reST-Zeichen escapen muessen.
Unser Testmodul ist:

.. literalinclude:: ../../examples-python/doc_escape.py
	:language: python
	:tab-width: 4

Der Docstring wird folgendermassen gerendert:

.. wtrl_autodoc_module:: doc_escape

Bestimmte Randfaelle wie in Sektion "Malformed Waterloo"
sind erwartbar auch in der Browserdarstellung problematisch.
Das tritt in der Praxis jedoch nur in dem exotischen Metafall auf,
dass man "falsche" Waterloo-Syntax in einem Docstring erklaeren
moechte.

Itemization
-----------

.. literalinclude:: ../../examples-python/doc_enumeration.py
	:language: python
	:tab-width: 4

.. wtrl_autodoc_function:: doc_enumeration.myfunc


