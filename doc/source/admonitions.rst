.. _chapter_admonitions:

Admonitions
===========

Error admonitions
-----------------

The following examples show how the renderer reports misuse or invalid input.

Inappropriate directive
~~~~~~~~~~~~~~~~~~~~~~~

.. wtrl_autodoc_class:: doc_errors

Pop on empty stack

.. wtrl_pop_current_module:: doc_errors

Push/pop mismatch

.. wtrl_push_current_module:: doc_errors

.. wtrl_pop_current_module:: doc_errors_wrong



Non-existing object
~~~~~~~~~~~~~~~~~~~

.. wtrl_autodoc_class:: doc_errors.X_does_not_exist

Missing docstring
~~~~~~~~~~~~~~~~~

.. wtrl_autodoc_class:: doc_errors.X_no_docstring

Empty docstring
~~~~~~~~~~~~~~~

.. wtrl_autodoc_class:: doc_errors.X_empty_docstring

Not a Waterloo Docstring
~~~~~~~~~~~~~~~~~~~~~~~~

.. wtrl_autodoc_class:: doc_errors.X_not_a_wtrl_docstring

Parsing or validation error
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. wtrl_autodoc_class:: doc_errors.X_bad_contract

Info admonitions
----------------

The following example shows an informational admonition emitted by the renderer.

.. _subsection_out_of_scope:

Out of scope
~~~~~~~~~~~~

.. wtrl_autodoc_class:: doc_errors.X_not_in_public_scope

Other admonitions
-----------------

The following example shows a state-change admonition.

State change
~~~~~~~~~~~~

.. wtrl_push_current_module:: doc_errors

.. wtrl_push_current_class:: X_no_docstring

.. wtrl_pop_current_class:: X_no_docstring

.. wtrl_pop_current_module:: doc_errors
