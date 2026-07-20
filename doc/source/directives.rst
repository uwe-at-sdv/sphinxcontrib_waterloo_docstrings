.. _chapter_directives:

Directives (todo)
=================

Es gibt drei Familien von Direktiven, die im folgenden besprochen werden,

* Direktiven zum Rendern von Docstrings
* Direktiven mit denen man den Zustand des Kontextes aendern kann innerhalb dessen das Dokument kompiliert wird.
* Direktiven zum Rendern von Signaturen

Docstring rendering directives (todo)
-------------------------------------

State changing directives
-------------------------

Die zustandsaendernden Direktiven sind:

* :wtrl_func:`.. wtrl_push_current_module::` :wtrl_var:`<module-identifier>`
* :wtrl_func:`.. wtrl_pop_current_module::` :wtrl_var:`<module-identifier>`
* :wtrl_func:`.. wtrl_push_current_class::` :wtrl_var:`<class-identifier>`
* :wtrl_func:`.. wtrl_pop_current_class::` :wtrl_var:`<class-identifier>`
* :wtrl_func:`.. wtrl_push_current_scope::` :wtrl_var:`<scope-symbol>`
* :wtrl_func:`.. wtrl_pop_current_scope::` :wtrl_var:`<scope-symbol>`

Diese Direktiven legen einen Wert auf den Module-, Class- oder Scope-Stack
oder entfernen den obersten Wert. Beim Entfernen wird als Konsistenztest
die Angabe des zu entfernenden Werts verlangt.


Module and class stack
~~~~~~~~~~~~~~~~~~~~~~

Die zustandsaendernden Direktiven dienen dazu, bei langen Listen von Render-Direktiven
die Nennung der Identifier zu vereinfachen. Statt Klassen so zu dokumentieren

.. code:: rst

	.. wtrl_autodoc_class:: sdv.doc.waterloo.docitem_helper.cls0

	.. wtrl_autodoc_class:: sdv.doc.waterloo.docitem_helper.cls1
	
	...

	.. wtrl_autodoc_class:: sdv.doc.waterloo.docitem_helper.cls<n>
	
legt man fest, dass :wtrl_mod:`sdv.doc.waterloo.docitem_helper` bis auf weiteres das Default-Modul ist,
bezueglich dessen Klassennamen aufgeloest werden:

.. code:: rst

	.. wtrl_push_current_module:: sdv.doc.waterloo.docitem_helper

	.. wtrl_autodoc_class:: cls0

	.. wtrl_autodoc_class:: cls1

	...
	
	.. wtrl_autodoc_class:: cls<n>

	.. wtrl_pop_current_module:: sdv.doc.waterloo.docitem_helper

Im Dokument werden diese Zustandwechsel so dargestellt.

.. wtrl_push_current_module:: sdv.doc.waterloo.docitem_helper

und

.. wtrl_pop_current_module:: sdv.doc.waterloo.docitem_helper

Intern werden die Modul-Identifier in einem Stack verwaltet. Einen solchen Stack gibt
es auch fuer Klassen, so dass man auch bei der Dokumentation von Methoden und eingebetteten
Klassen etwas weniger Redundanz hat. Statt

.. code:: rst

	.. wtrl_autodoc_method:: sdv.doc.waterloo.docitem_helper.tracer.meth0

	.. wtrl_autodoc_method:: sdv.doc.waterloo.docitem_helper.tracer.meth1
	
	...

	.. wtrl_autodoc_method:: sdv.doc.waterloo.docitem_helper.tracer.meth<n>

schreibt man	

.. code:: rst

	.. wtrl_push_current_class:: sdv.doc.waterloo.docitem_helper.tracer

	.. wtrl_autodoc_method:: meth0

	.. wtrl_autodoc_method:: meth1

	...
	
	.. wtrl_autodoc_method:: meth<n>

	.. wtrl_pop_current_module:: sdv.doc.waterloo.docitem_helper.tracer

Analog zum Modulstack werden Aenderungen im Dokument dargestellt:

.. wtrl_push_current_class:: sdv.doc.waterloo.docitem_helper.tracer

und

.. wtrl_pop_current_class:: sdv.doc.waterloo.docitem_helper.tracer

Scope stack
~~~~~~~~~~~

Die dritte Direktive in dieser Familie dient dazu, den Scope festzulegen.
Dokumentationen aus Waterloo Docstrings koennen auf eine bestimmte Zielgruppe
zugeschnitten werden, die durch den Scope zum Ausdruck gebracht wird.
(siehe <Link zum Waterloo-Standard-Dokument>)

Durch die Direktive

.. code:: rst

	.. wtrl_push_current_scope:: public

als Beispiel wird festgelegt, dass ab jetzt nur noch Objekte mit dem Scope :wtrl_value:`public`
dargestellt werden. Die Scopes bilden eine (partielle geordnete) Hierarchie

.. code:: text

	core > extension > public

wie im folgenden klar weden sollte. Der Aufruf

.. code:: rst

	.. wtrl_push_current_scope:: extension

zeigt alle Objekte, die mit :wtrl_value:`extension` oder :wtrl_value:`public` markiert sind.
Der Aufruf

.. code:: rst

	.. wtrl_push_current_scope:: core

zeigt alle Objekte, also :wtrl_value:`core`, :wtrl_value:`extension` und :wtrl_value:`public`.
Auch diese Zustandswechsel werden im Dokument dargestellt.

.. wtrl_push_current_scope:: extension

.. wtrl_pop_current_scope:: extension

In der Praxis wird man oft den Scope zu Beginn des Dokuments festlegen und danach nicht mehr aendern.


Directives for rendering callable signature
-------------------------------------------

Die Direktiven zum Rendern von Signaturen sind:

* :wtrl_func:`.. wtrl_function_signature::` :wtrl_var:`<function-identifier>`
* :wtrl_func:`.. wtrl_function_signature_block::` :wtrl_var:`<function-identifier>`
* :wtrl_func:`.. wtrl_method_signature::` :wtrl_var:`<method-identifier>`
* :wtrl_func:`.. wtrl_method_signature_block::` :wtrl_var:`<method-identifier>`


.. wtrl_push_current_module:: sphinxcontrib.waterloo_docstrings

We render the function :wtrl_func:`resolve_qualified_name` from this extension
for demonstration and testing purposes.
A function signature is rendered as inline element by the following directive:

.. code:: rst

	.. wtrl_function_signature:: extension.resolve_qualified_name

which leads to

.. wtrl_function_signature:: extension.resolve_qualified_name

This might be sufficient for small signatures, yet in general
a block element is more appropriate:

.. code:: rst

	.. wtrl_function_signature_block:: extension.resolve_qualified_name

.. wtrl_function_signature_block:: extension.resolve_qualified_name

.. wtrl_pop_current_module:: sphinxcontrib.waterloo_docstrings

For methods we have similar directives. As an example we render
the signature of a method in the tracer class from module :wtrl_mod:`docitem_helper`
in package :wtrl_pkg:`sdv.doc.waterloo`:

.. code:: rst

	.. wtrl_method_signature:: sdv.doc.waterloo.docitem_helper.tracer.build_json

which leads to

.. wtrl_method_signature:: sdv.doc.waterloo.docitem_helper.tracer.build_json

or in block representation:

.. code:: rst

	.. wtrl_method_signature_block:: sdv.doc.waterloo.docitem_helper.tracer.build_json

which leads to

.. wtrl_method_signature_block:: sdv.doc.waterloo.docitem_helper.tracer.build_json
