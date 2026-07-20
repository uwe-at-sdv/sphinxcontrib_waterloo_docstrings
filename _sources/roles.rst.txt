.. _chapter_roles:

Roles
=====

Semantic Markup
---------------

Das folgende Modul demonstriert, wie man Roles in Docstrings verwendet.
Die Schreibweise innerhalb von Docstrings ist allgemein :wtrl_lit:`|role|\`par\``, also
der Name der Role in Pipedelimitern gefolgt von einem stringwertigen Parameter
von Backticks umrahmt.

.. wtrl_autodoc_module:: doc_roles

Der Waterloo-Compiler uebersetzt diese Roles in normale reST-Roles.
Diese Roles kann man auch im Fliesstext verwenden. Thematisch
gibt es dabei Ueberschneidungen mit dem Grundbestand von Sphinx.
Es bleibt dem Autor ueberlassen, welche Roles er verwenden moechte.
Fuer die Maschinenlesbarkeit ist nur entscheidend, dass die spezielle
Notation von Waterloo in Docstrings verwendet wird.

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

The Waterloo Docstring format offers a certain set of normativity keywords inspired by
RFC-2119 (omitting however MAY NOT, since this is semantically ambiguous).
Also, there is a small set of values in tokenzied form. The following module rendering
gives a comprehensive overview on these tokens.

.. wtrl_autodoc_module:: doc_normativity_and_value_tokens


Cross referencing
-----------------

Mit den folgenden Klassen des Module :wtrl_mod:`doc_cross_referencing` in :wtrl_file:`${REPO}/examples-python`
testen wir umfassend die diversen Faelle von Cross-References.

* Referenzen auf andere Objekte innerhalb des Moduls
	* Mittels Identifier
	* Mittels Qualified Identifier (Modul + Objekt)
* Referenzen auf andere Objekte ausserhalb des Moduls
	* Mittels Fully Qualified Identifier (Package + Modul + Objekt)
* Referenzen auf Label im umgebenden Sphinx-Dokument
	* im selben File
	* in einem anderen File
* Referenzen auf Web-Seiten (HTTP / HTTPS)
* Referenzen auf nicht-existente Targets

Beachte, auf welche Weise die Referenz aufgebaut wird:

* :wtrl_lit:`|ref|`Label <wtrl://...>`` -- Schema :wtrl_lit:`wtrl://` fuer Objekte mit Waterloo Docstrings.
* :wtrl_lit:`|ref|`label <http[s]://...>`` -- Schema :wtrl_lit:`http://` oder :wtrl_lit:`https://` fuer Webseiten
* :wtrl_lit:`|ref|`Label <...>`` -- ohne Schema, fuer Referenzen innerhalb des Projekts


.. wtrl_push_current_module:: doc_cross_referencing

.. wtrl_autodoc_class:: A

.. wtrl_autodoc_class:: B

.. wtrl_pop_current_module:: doc_cross_referencing
