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

Function :wtrl_func:`build_sphinx_nodes`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. wtrl_autodoc_function:: build_sphinx_nodes


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
