.. _chapter_admonitions:

Admonitions
===========

The Waterloo extension can render diagnostics and context changes directly into
the generated document. This is especially useful while writing documentation:
the message appears close to the directive that caused it, instead of only
being visible in the terminal output.

This chapter intentionally contains broken directives and invalid docstrings.
The resulting admonitions are part of the showcase.


Error Admonitions
-----------------

Error admonitions report directive misuse, unresolved objects, missing
docstrings, and Waterloo parsing or validation errors. They are controlled by
:wtrl_var:`wtrl_diagnostics_admonitions_enabled`.


Inappropriate Directive
~~~~~~~~~~~~~~~~~~~~~~~

The following directive asks for a class, but the identifier resolves to a
module. The renderer therefore emits a directive diagnostic instead of trying
to render the module as a class.

.. wtrl_autodoc_class:: doc_errors


Pop On Empty Stack
~~~~~~~~~~~~~~~~~~

The context stacks are checked strictly. Popping the current module while the
module stack is empty produces a diagnostic admonition.

.. wtrl_pop_current_module:: doc_errors


Push/Pop Mismatch
~~~~~~~~~~~~~~~~~

Pop directives require the value that is expected at the top of the stack. This
turns accidental nesting mistakes into visible diagnostics.

.. wtrl_push_current_module:: doc_errors

.. wtrl_pop_current_module:: doc_errors_wrong


Non-Existing Object
~~~~~~~~~~~~~~~~~~~

If the identifier cannot be resolved, the renderer reports the failed object
lookup at the directive location.

.. wtrl_autodoc_class:: doc_errors.X_does_not_exist


Missing Docstring
~~~~~~~~~~~~~~~~~

An object without a docstring cannot be rendered as Waterloo documentation. The
directive therefore emits a diagnostic instead of silently producing no output.

.. wtrl_autodoc_class:: doc_errors.X_no_docstring


Empty Docstring
~~~~~~~~~~~~~~~

An empty docstring is treated like a missing documentation body and is reported
explicitly.

.. wtrl_autodoc_class:: doc_errors.X_empty_docstring


Not A Waterloo Docstring
~~~~~~~~~~~~~~~~~~~~~~~~

The following class has a Python docstring, but the text is not a valid
Waterloo docstring. The parser diagnostic is shown in the generated document.

.. wtrl_autodoc_class:: doc_errors.X_not_a_wtrl_docstring


Parsing Or Validation Error
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The next example is syntactically close to a Waterloo docstring, but its
content fails validation. The rendered admonition preserves the structured
Waterloo diagnostic, including rule id, found/expected information, and hint.

.. wtrl_autodoc_class:: doc_errors.X_bad_contract


Info Admonitions
----------------

Not every rendered admonition indicates an error. Some messages describe
intentional omissions or visible state changes.

.. _subsection_out_of_scope:

Out Of Scope
~~~~~~~~~~~~

The following object exists and has a Waterloo docstring, but it is assigned a
scope that is not visible under the current documentation scope. If
:wtrl_var:`wtrl_scope_filtered_object_placeholders_enabled` is enabled, the
renderer leaves a placeholder admonition instead of removing the object without
a trace.

.. wtrl_autodoc_class:: doc_errors.X_not_in_public_scope


State-Change Admonitions
------------------------

State-changing directives can also be rendered into the document. This is
controlled by :wtrl_var:`wtrl_state_change_admonitions_enabled`.

The following sequence shows module and class context changes as they appear in
the generated document.

.. wtrl_push_current_module:: doc_errors

.. wtrl_push_current_class:: X_no_docstring

.. wtrl_pop_current_class:: X_no_docstring

.. wtrl_pop_current_module:: doc_errors
