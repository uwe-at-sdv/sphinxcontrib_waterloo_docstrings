.. _chapter_roles:

Roles
=====

Semantic Markup
---------------

The following module demonstrates how to use roles in docstrings.
The general Waterloo notation inside docstrings is
:wtrl_lit:`|role|\`par\``, that is, the role name in pipe delimiters followed
by a string-valued parameter enclosed in backticks.

.. wtrl_autodoc_module:: doc_roles

The Waterloo renderer converts these roles into ordinary reST roles.
You can also use these roles in running text. Some of them overlap
conceptually with the standard Sphinx role set. It is up to the author to
choose the roles that best express the intended meaning. For machine
readability, the important part is simply that the Waterloo notation is used
inside docstrings.

.. list-table::
	:header-rows: 1
	:widths: 35 65

	* - Rendered
	  - Code
	* - :wtrl_attr:`abc`, :wtrl_attr:`ABC`
	  - :literal:`:wtrl_attr:\`abc\`, :wtrl_attr:\`ABC\``
	* - :wtrl_class:`abc`, :wtrl_class:`ABC`
	  - :literal:`:wtrl_class:\`abc\`, :wtrl_class:\`ABC\``
	* - :wtrl_cmd:`abc`, :wtrl_cmd:`ABC`
	  - :literal:`:wtrl_cmd:\`abc\`, :wtrl_cmd:\`ABC\``
	* - :wtrl_dfn:`abc`, :wtrl_dfn:`ABC`
	  - :literal:`:wtrl_dfn:\`abc\`, :wtrl_dfn:\`ABC\``
	* - :wtrl_file:`/path/to/abc`, :wtrl_file:`S:\\ABC`
	  - :literal:`:wtrl_file:\`/path/to/abc\`, :wtrl_file:\`S:\\\\ABC\``
	* - :wtrl_func:`print`, :wtrl_func:`MyClass.my_method`
	  - :literal:`:wtrl_func:\`print\`, :wtrl_func:\`MyClass.my_method\``
	* - :wtrl_key:`Q`, :wtrl_key:`CTRL` + :wtrl_key:`Z`
	  - :literal:`:wtrl_key:\`Q\`, :wtrl_key:\`CTRL\` + :wtrl_key:\`Z\``
	* - :wtrl_label:`abc`, :wtrl_label:`ABC`
	  - :literal:`:wtrl_label:\`abc\`, :wtrl_label:\`ABC\``
	* - :wtrl_lit:`abc`, :wtrl_lit:`ABC`
	  - :literal:`:wtrl_lit:\`abc\`, :wtrl_lit:\`ABC\``
	* - :wtrl_mod:`abc`, :wtrl_mod:`ABC`
	  - :literal:`:wtrl_mod:\`abc\`, :wtrl_mod:\`ABC\``
	* - :wtrl_norm:`Should`, :wtrl_norm:`must`
	  - :literal:`:wtrl_norm:\`Should\`, :wtrl_norm:\`must\``
	* - :wtrl_op:`+`, :wtrl_op:`*`
	  - :literal:`:wtrl_op:\`+\`, :wtrl_op:\`*\``
	* - :wtrl_opt:`-a`, :wtrl_opt:`--no-debug`
	  - :literal:`:wtrl_opt:\`-a\`, :wtrl_opt:\`--no-debug\``
	* - :wtrl_pkg:`abc`, :wtrl_pkg:`ABC`
	  - :literal:`:wtrl_pkg:\`abc\`, :wtrl_pkg:\`ABC\``
	* - :wtrl_tag:`abc`, :wtrl_tag:`ABC`
	  - :literal:`:wtrl_tag:\`abc\`, :wtrl_tag:\`ABC\``
	* - :wtrl_term:`Unicorn`
	  - :literal:`:wtrl_term:\`Unicorn\``
	* - :wtrl_type:`float`, :wtrl_type:`BaseException`
	  - :literal:`:wtrl_type:\`float\`, :wtrl_type:\`BaseException\``
	* - :wtrl_url:`https://github.com`
	  - :literal:`:wtrl_url:\`https://github.com\``
	* - :wtrl_value:`12345`, :wtrl_value:`"ABC"`
	  - :literal:`:wtrl_value:\`12345\`, :wtrl_value:\`"ABC"\``
	* - :wtrl_var:`use_color`, :wtrl_var:`PATH`
	  - :literal:`:wtrl_var:\`use_color\`, :wtrl_var:\`PATH\``
	* - :wtrl_var_type:`use_color:bool`
	  - :literal:`:wtrl_var_type:\`use_color:bool\``


Normativity and value tokens
----------------------------

The Waterloo Docstring format offers a fixed set of normativity keywords
inspired by RFC 2119. `MAY NOT` is intentionally omitted because it is
semantically ambiguous in this context. The format also defines a small set of
values in tokenized form. The following module rendering gives a compact
overview of these tokens.

.. wtrl_autodoc_module:: doc_normativity_and_value_tokens


Cross referencing
-----------------

The following classes from the module :wtrl_mod:`doc_cross_referencing` in
:wtrl_file:`${REPO}/examples-python` demonstrate the different forms of
cross-references.

* References to other objects within the module
	* By identifier
	* By qualified identifier (module + object)
* References to other objects outside the module
	* By fully qualified identifier (package + module + object)
* References to labels in the surrounding Sphinx document
	* in the same file
	* in a different file
* References to web pages (HTTP / HTTPS)
* References to non-existent targets

Pay attention to how the reference target is written:

* :wtrl_lit:`|ref|`Label <wtrl://...>`` -- use :wtrl_lit:`wtrl://` for Waterloo docstring objects.
* :wtrl_lit:`|ref|`label <http[s]://...>`` -- use :wtrl_lit:`http://` or :wtrl_lit:`https://` for web pages.
* :wtrl_lit:`|ref|`Label <...>`` -- omit the scheme for references within the project.


.. wtrl_push_current_module:: doc_cross_referencing

.. wtrl_autodoc_class:: A

.. wtrl_autodoc_class:: B

.. wtrl_pop_current_module:: doc_cross_referencing
