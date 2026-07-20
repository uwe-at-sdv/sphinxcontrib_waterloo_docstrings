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

Der Docstring wird folgendermassen gerendert:

.. wtrl_autodoc_module:: doc_escape

Bestimmte Randfaelle wie in Sektion "Malformed Waterloo"
sind erwartbar auch in der Browserdarstellung problematisch.
Das tritt in der Prax jedoch nur in dem exotischen Metafall auf,
dass man "falsche" Waterloo-Syntax in einem Docstring erklaeren
moechte.
