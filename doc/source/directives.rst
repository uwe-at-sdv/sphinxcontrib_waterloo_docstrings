.. _chapter_directives:

Directives
==========

Waterloo directives insert generated documentation into a Sphinx document or
change the build-time context used by later directives. They are ordinary reST
directives with one argument and no directive body.

The extension provides three directive families:

* Docstring rendering directives
* State-changing directives
* Callable signature directives


Docstring Rendering Directives
------------------------------

The docstring rendering directives are:

* :wtrl_func:`.. wtrl_autodoc_module::` :wtrl_var:`<module-identifier>`
* :wtrl_func:`.. wtrl_autodoc_class::` :wtrl_var:`<class-identifier>`
* :wtrl_func:`.. wtrl_autodoc_function::` :wtrl_var:`<function-identifier>`
* :wtrl_func:`.. wtrl_autodoc_method::` :wtrl_var:`<method-identifier>`

and the special recursive directive:

* :wtrl_func:`.. wtrl_autodoc_class_full::` :wtrl_var:`<class-identifier>`

Each directive resolves its argument to a Python object, reads that object's
Waterloo docstring, validates it, and renders it as Docutils nodes. Resolution
uses the current Python interpreter, the configured :wtrl_var:`wtrl_basedirs`,
and the current module/class state described below.

The identifier may be plain, partially qualified, or fully qualified. Fully
qualified identifiers are explicit and work independently of the current state:

.. code:: rst

	.. wtrl_autodoc_class:: sdv.doc.waterloo.docitem_helper.tracer

Plain identifiers become practical once a current module or class has been
pushed:

.. code:: rst

	.. wtrl_push_current_module:: sdv.doc.waterloo.docitem_helper

	.. wtrl_autodoc_class:: tracer

	.. wtrl_pop_current_module:: sdv.doc.waterloo.docitem_helper

The directive :wtrl_func:`.. wtrl_autodoc_class_full::` starts with the class
itself and then renders documentable member classes and methods recursively. It
is useful for compact reference pages, while :wtrl_func:`.. wtrl_autodoc_class::`
is better when the surrounding document should control the order and grouping
of members manually.

The extension module :ref:`reference <chapter_reference>` demonstrates the
effect of these directives. Theme-specific showcase builds are available for:

* `the classic theme <https://uwe-at-sdv.github.io/sphinxcontrib_waterloo_docstrings/showcase/classic/>`_
* `the alabaster theme <https://uwe-at-sdv.github.io/sphinxcontrib_waterloo_docstrings/showcase/alabaster/>`_
* `the furo theme <https://uwe-at-sdv.github.io/sphinxcontrib_waterloo_docstrings/showcase/furo/>`_


.. _section_state_changing_directives:

State-Changing Directives
-------------------------

The state-changing directives are:

* :wtrl_func:`.. wtrl_push_current_module::` :wtrl_var:`<module-identifier>`
* :wtrl_func:`.. wtrl_pop_current_module::` :wtrl_var:`<module-identifier>`
* :wtrl_func:`.. wtrl_push_current_class::` :wtrl_var:`<class-identifier>`
* :wtrl_func:`.. wtrl_pop_current_class::` :wtrl_var:`<class-identifier>`
* :wtrl_func:`.. wtrl_push_current_scope::` :wtrl_var:`<scope-symbol>`
* :wtrl_func:`.. wtrl_pop_current_scope::` :wtrl_var:`<scope-symbol>`

These directives maintain three independent stacks: current module, current
class, and current scope. A push directive adds a value to the corresponding
stack. A pop directive removes the top value and requires the expected value as
its argument. This explicit pop argument is intentional: it turns accidental
nesting mistakes into visible diagnostics.

Depending on the configuration, state changes are rendered as small
admonitions and/or logged during the Sphinx build. See
:ref:`Configuration <chapter_configuration>` for the corresponding switches.


Module And Class Stack
~~~~~~~~~~~~~~~~~~~~~~

The module and class stacks reduce repetition in long sequences of rendering
directives. Instead of writing fully qualified names for every class:

.. code:: rst

	.. wtrl_autodoc_class:: sdv.doc.waterloo.docitem_helper.cls0

	.. wtrl_autodoc_class:: sdv.doc.waterloo.docitem_helper.cls1

	...

	.. wtrl_autodoc_class:: sdv.doc.waterloo.docitem_helper.clsN

you can push the module once and document the classes by their local names:

.. code:: rst

	.. wtrl_push_current_module:: sdv.doc.waterloo.docitem_helper

	.. wtrl_autodoc_class:: cls0

	.. wtrl_autodoc_class:: cls1

	...

	.. wtrl_autodoc_class:: clsN

	.. wtrl_pop_current_module:: sdv.doc.waterloo.docitem_helper

In the rendered document, the module state change looks like this:

.. wtrl_push_current_module:: sdv.doc.waterloo.docitem_helper

and is closed as follows:

.. wtrl_pop_current_module:: sdv.doc.waterloo.docitem_helper

The class stack works in the same way and is mainly useful for methods and
nested classes. Instead of writing fully qualified method identifiers:

.. code:: rst

	.. wtrl_autodoc_method:: sdv.doc.waterloo.docitem_helper.tracer.meth0

	.. wtrl_autodoc_method:: sdv.doc.waterloo.docitem_helper.tracer.meth1

	...

	.. wtrl_autodoc_method:: sdv.doc.waterloo.docitem_helper.tracer.methN

you can push the module and class once:

.. code:: rst

	.. wtrl_push_current_module:: sdv.doc.waterloo.docitem_helper

	.. wtrl_push_current_class:: tracer

	.. wtrl_autodoc_method:: meth0

	.. wtrl_autodoc_method:: meth1

	...

	.. wtrl_autodoc_method:: methN

	.. wtrl_pop_current_class:: tracer

	.. wtrl_pop_current_module:: sdv.doc.waterloo.docitem_helper

The corresponding state changes are rendered as follows:

.. wtrl_push_current_module:: sdv.doc.waterloo.docitem_helper

.. wtrl_push_current_class:: tracer

and are closed as follows:

.. wtrl_pop_current_class:: tracer

.. wtrl_pop_current_module:: sdv.doc.waterloo.docitem_helper


Scope Stack
~~~~~~~~~~~

The scope stack controls which docstrings are visible in the generated
document. Waterloo docstrings may declare a scope, and a Sphinx document can
select the target audience by pushing a scope value.

The current scope order is:

.. code:: text

	core > extension > public

Choosing :wtrl_value:`public` renders only public documentation:

.. code:: rst

	.. wtrl_push_current_scope:: public

Choosing :wtrl_value:`extension` also includes extension-level documentation:

.. code:: rst

	.. wtrl_push_current_scope:: extension

Choosing :wtrl_value:`core` renders the most complete view, including core,
extension, and public documentation:

.. code:: rst

	.. wtrl_push_current_scope:: core

The following state change is rendered into this documentation for
demonstration purposes:

.. wtrl_push_current_scope:: extension

.. wtrl_pop_current_scope:: extension

In practice, you will often set the scope near the beginning of a reference
page and leave it unchanged afterwards.


Callable Signature Directives
-----------------------------

The callable signature directives render a Python signature without rendering
the full Waterloo docstring:

* :wtrl_func:`.. wtrl_function_signature::` :wtrl_var:`<function-identifier>`
* :wtrl_func:`.. wtrl_function_signature_block::` :wtrl_var:`<function-identifier>`
* :wtrl_func:`.. wtrl_method_signature::` :wtrl_var:`<method-identifier>`
* :wtrl_func:`.. wtrl_method_signature_block::` :wtrl_var:`<method-identifier>`

Use the inline variants when the signature is short enough to fit naturally
into running text. Use the block variants for longer signatures or when the
signature should visually introduce a following explanation.

.. wtrl_push_current_module:: sphinxcontrib.waterloo_docstrings

For demonstration and testing, this document renders the function
:wtrl_func:`resolve_qualified_name` from the extension package. The inline
directive is written as:

.. code:: rst

	.. wtrl_function_signature:: extension.resolve_qualified_name

and renders as:

.. wtrl_function_signature:: extension.resolve_qualified_name

The block form is written as:

.. code:: rst

	.. wtrl_function_signature_block:: extension.resolve_qualified_name

and renders as:

.. wtrl_function_signature_block:: extension.resolve_qualified_name

.. wtrl_pop_current_module:: sphinxcontrib.waterloo_docstrings

Method signatures work analogously. The following example renders a method in
the :wtrl_class:`tracer` class from :wtrl_mod:`sdv.doc.waterloo.docitem_helper`:

.. code:: rst

	.. wtrl_method_signature:: sdv.doc.waterloo.docitem_helper.tracer.build_json

which renders as:

.. wtrl_method_signature:: sdv.doc.waterloo.docitem_helper.tracer.build_json

The block representation is written as:

.. code:: rst

	.. wtrl_method_signature_block:: sdv.doc.waterloo.docitem_helper.tracer.build_json

and renders as:

.. wtrl_method_signature_block:: sdv.doc.waterloo.docitem_helper.tracer.build_json
