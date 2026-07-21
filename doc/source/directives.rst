.. _chapter_directives:

Directives
==========

There are three families of directives, which are discussed below:

* Directives for rendering docstrings
* Directives that allow you to modify the state of the context during document compilation.
* Directives for rendering signatures

Docstring rendering directives
------------------------------

The directives for rendering docstrings are:

* :wtrl_func:`.. wtrl_autodoc_module::` :wtrl_var:`<module-identifier>`
* :wtrl_func:`.. wtrl_autodoc_class::` :wtrl_var:`<class-identifier>`
* :wtrl_func:`.. wtrl_autodoc_function::` :wtrl_var:`<function-identifier>`
* :wtrl_func:`.. wtrl_autodoc_method::` :wtrl_var:`<method-identifier>`

and the special directive

* :wtrl_func:`.. wtrl_autodoc_class_full::` :wtrl_var:`<class-identifier>`

The argument is a plain, partially or fully qualified identifier.
In combination with the :ref:`state changing directives <section_state_changing_directives>`
a plain or partially qualified identifier is sufficient. The extension module
:ref:`reference <chapter_reference>` demonstrates the effect of these directives.
Also, please have a look at the showcases for

* `the classic theme <https://uwe-at-sdv.github.io/sphinxcontrib_waterloo_docstrings/showcase/classic/>`_
* `the alabaster theme <https://uwe-at-sdv.github.io/sphinxcontrib_waterloo_docstrings/showcase/alabaster/>`_
* `the furo theme <https://uwe-at-sdv.github.io/sphinxcontrib_waterloo_docstrings/showcase/furo/>`_


.. _section_state_changing_directives:

State changing directives
-------------------------

The state changing directives are:

* :wtrl_func:`.. wtrl_push_current_module::` :wtrl_var:`<module-identifier>`
* :wtrl_func:`.. wtrl_pop_current_module::` :wtrl_var:`<module-identifier>`
* :wtrl_func:`.. wtrl_push_current_class::` :wtrl_var:`<class-identifier>`
* :wtrl_func:`.. wtrl_pop_current_class::` :wtrl_var:`<class-identifier>`
* :wtrl_func:`.. wtrl_push_current_scope::` :wtrl_var:`<scope-symbol>`
* :wtrl_func:`.. wtrl_pop_current_scope::` :wtrl_var:`<scope-symbol>`

These directives push a value onto the module, class, or scope stack or remove
the top value. When removing a value, a consistency check requires that the
value to be removed be specified.


Module and class stack
~~~~~~~~~~~~~~~~~~~~~~

The state-changing directives are used to simplify the listing of identifiers
in long lists of render directives. Instead of documenting classes as follows

.. code:: rst

	.. wtrl_autodoc_class:: sdv.doc.waterloo.docitem_helper.cls0

	.. wtrl_autodoc_class:: sdv.doc.waterloo.docitem_helper.cls1
	
	...

	.. wtrl_autodoc_class:: sdv.doc.waterloo.docitem_helper.cls<n>
	
you specify that, in this example, :wtrl_mod:`sdv.doc.waterloo.docitem_helper`
is the default module until the next state change, and that its class names are
resolved as follows:

.. code:: rst

	.. wtrl_push_current_module:: sdv.doc.waterloo.docitem_helper

	.. wtrl_autodoc_class:: cls0

	.. wtrl_autodoc_class:: cls1

	...
	
	.. wtrl_autodoc_class:: cls<n>

	.. wtrl_pop_current_module:: sdv.doc.waterloo.docitem_helper

In the document, these state changes are represented as follows:

.. wtrl_push_current_module:: sdv.doc.waterloo.docitem_helper

and

.. wtrl_pop_current_module:: sdv.doc.waterloo.docitem_helper

Internally, the module identifiers are managed in a stack. A similar stack
also exists for classes, so there is slightly less redundancy when documenting
methods and nested classes. Instead of

.. code:: rst

	.. wtrl_autodoc_method:: sdv.doc.waterloo.docitem_helper.tracer.meth0

	.. wtrl_autodoc_method:: sdv.doc.waterloo.docitem_helper.tracer.meth1
	
	...

	.. wtrl_autodoc_method:: sdv.doc.waterloo.docitem_helper.tracer.meth<n>

you write	

.. code:: rst

	.. wtrl_push_current_module:: sdv.doc.waterloo.docitem_helper

	.. wtrl_push_current_class:: tracer

	.. wtrl_autodoc_method:: meth0

	.. wtrl_autodoc_method:: meth1

	...
	
	.. wtrl_autodoc_method:: meth<n>

	.. wtrl_pop_current_class:: tracer

	.. wtrl_pop_current_module:: sdv.doc.waterloo.docitem_helper

Changes in the document are displayed in a manner analogous to the module and
class stacks:

.. wtrl_push_current_module:: sdv.doc.waterloo.docitem_helper

.. wtrl_push_current_class:: tracer

and

.. wtrl_pop_current_class:: tracer

.. wtrl_pop_current_module:: sdv.doc.waterloo.docitem_helper

Scope stack
~~~~~~~~~~~

The third directive in this family is used to define the scope. Documentation
generated from Waterloo docstrings can be tailored to a specific target
audience, which is expressed by the scope, as specified in the Waterloo
`standard document <https://uwe-at-sdv.github.io/sdv_doc_waterloo/>`_.

The directive

.. code:: rst

	.. wtrl_push_current_scope:: public

specifies, as an example, that from now on only objects with the scope
:wtrl_value:`public` will be displayed. The scopes form a partially ordered
hierarchy

.. code:: text

	core > extension > public

as should become clear below. The call

.. code:: rst

	.. wtrl_push_current_scope:: extension

pushes the scope down one level. The call

.. code:: rst

	.. wtrl_push_current_scope:: core

displays all objects marked with :wtrl_value:`extension` or
:wtrl_value:`public`. These state changes are also displayed in the document.

.. wtrl_push_current_scope:: extension

.. wtrl_pop_current_scope:: extension

In practice, you will often set the scope at the beginning of the document and
leave it unchanged afterward.


Directives for rendering callable signatures
--------------------------------------------

The directives for rendering signatures are:

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

For methods we have similar directives. As an example we render the signature
of a method in the tracer class from module :wtrl_mod:`docitem_helper` in
package :wtrl_pkg:`sdv.doc.waterloo`:

.. code:: rst

	.. wtrl_method_signature:: sdv.doc.waterloo.docitem_helper.tracer.build_json

which leads to

.. wtrl_method_signature:: sdv.doc.waterloo.docitem_helper.tracer.build_json

or in block representation:

.. code:: rst

	.. wtrl_method_signature_block:: sdv.doc.waterloo.docitem_helper.tracer.build_json

which leads to

.. wtrl_method_signature_block:: sdv.doc.waterloo.docitem_helper.tracer.build_json
