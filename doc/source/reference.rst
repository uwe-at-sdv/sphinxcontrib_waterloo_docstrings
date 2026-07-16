Reference
=========

In this chapter we present the self-referential documentation
of the sphinx extension, by means of the sphinx extension.
For state changes we have added notes indicating the reequired reST-code.
Note that state changes require the fully qualified name of the module/class
to be push to/popped from the state stack.

The code for the following state change is

.. code:: rst

	.. wtrl_push_current_scope:: core

.. wtrl_push_current_scope:: core

The code for the following state change is

.. code:: rst

	.. wtrl_push_current_module:: sphinxcontrib.waterloo_docstrings

.. wtrl_push_current_module:: sphinxcontrib.waterloo_docstrings

Module :wtrl_mod:`extension`
----------------------------

.. wtrl_autodoc_module:: extension

The code for the following state change is

.. code:: rst

	.. wtrl_push_current_module:: sphinxcontrib.waterloo_docstrings.extension

.. wtrl_push_current_module:: sphinxcontrib.waterloo_docstrings.extension

Helper
~~~~~~

Function :wtrl_func:`resolve_qualified_name`
............................................

.. wtrl_autodoc_function:: resolve_qualified_name

Function :wtrl_func:`build_sphinx_nodes`
........................................

.. wtrl_autodoc_function:: build_sphinx_nodes

Function :wtrl_func:`build_sphinx_nodes_full`
.............................................

.. wtrl_autodoc_function:: build_sphinx_nodes_full


Directives for docstring rendering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. wtrl_autodoc_function:: wtrl_build_autodoc_module_nodes

.. wtrl_autodoc_function:: wtrl_build_autodoc_class_nodes

.. wtrl_autodoc_function:: wtrl_build_autodoc_function_nodes

.. wtrl_autodoc_function:: wtrl_build_autodoc_class_full_nodes

Directives for controlling the state stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scope stack
...........

.. wtrl_autodoc_function:: wtrl_build_push_current_scope_nodes

.. wtrl_autodoc_function:: wtrl_build_pop_current_scope_nodes

Module stack
............

.. wtrl_autodoc_function:: wtrl_build_push_current_module_nodes

.. wtrl_autodoc_function:: wtrl_build_pop_current_module_nodes

Class stack
...........

.. wtrl_autodoc_function:: wtrl_build_push_current_class_nodes

.. wtrl_autodoc_function:: wtrl_build_pop_current_class_nodes

Directives for rendering signatures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Function :wtrl_func:`wtrl_build_method_signature_nodes`
.......................................................

.. wtrl_autodoc_function:: wtrl_build_method_signature_nodes

Function :wtrl_func:`wtrl_build_function_signature_nodes`
.........................................................

.. wtrl_autodoc_function:: wtrl_build_function_signature_nodes

Function :wtrl_func:`wtrl_build_method_signature_block_nodes`
.............................................................

.. wtrl_autodoc_function:: wtrl_build_method_signature_block_nodes

Function :wtrl_func:`wtrl_build_function_signature_block_nodes`
...............................................................

.. wtrl_autodoc_function:: wtrl_build_function_signature_block_nodes

Roles for semantic markup
~~~~~~~~~~~~~~~~~~~~~~~~~

Function :wtrl_func:`wtrl_attr_role`
........................................

.. wtrl_autodoc_function:: wtrl_attr_role

Similar roles
.............

There are around 15 more role implementations like :wtrl_func:`wtrl_attr_role`,
which only differ in the CSS class passed and the :wtrl_pkg:`docutil` node classes
:wtrl_class:`literal` vs :wtrl_class:`inline`. We skip these here in order
to keep the document at low redundancy.

Function :wtrl_func:`wtrl_var_type_role`
........................................

.. wtrl_autodoc_function:: wtrl_var_type_role




The code for the following state change is

.. code:: rst

	.. wtrl_pop_current_module:: sphinxcontrib.waterloo_docstrings.extension

.. wtrl_pop_current_module:: sphinxcontrib.waterloo_docstrings.extension

The code for the following state change is

.. code:: rst

	.. wtrl_pop_current_module:: sphinxcontrib.waterloo_docstrings

.. wtrl_pop_current_module:: sphinxcontrib.waterloo_docstrings

The code for the following state change is

.. code:: rst

	.. wtrl_pop_current_scope:: core

.. wtrl_pop_current_scope:: core
